"""本地 ResNet18 花卉识别推理服务。

加载 model_assets/flower-resnet18 下的权重与标签，执行 224×224 预处理并返回 Top-5 候选。
详见 docs/FLOWER_MODEL.md。
"""
import io
import json
import threading
from pathlib import Path

import torch
from PIL import Image, ImageDraw, ImageFont, ImageOps
from torchvision import models, transforms


class FlowerService:
    model_id = 'flower-resnet18-5class@2026-09-20'

    def __init__(self, model_dir, device='cpu', num_threads=4):
        model_dir = Path(model_dir)
        self.labels = json.loads((model_dir / 'labels.json').read_text(encoding='utf-8'))
        if [label['id'] for label in self.labels] != list(range(5)):
            raise ValueError('花卉模型标签必须按训练索引 0–4 排列')
        self.class_names = [label['name'] for label in self.labels]
        self.device = torch.device(device)
        if self.device.type == 'cpu':
            torch.set_num_threads(max(1, num_threads))
        self.model = models.resnet18(weights=None, num_classes=len(self.labels))
        state = torch.load(model_dir / 'best-ckpt2.pt', map_location='cpu', weights_only=True)
        self.model.load_state_dict(state, strict=True)
        self.model.to(self.device).eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ])
        self.lock = threading.Lock()

    def _predict(self, img_bytes):
        with Image.open(io.BytesIO(img_bytes)) as source:
            img = ImageOps.exif_transpose(source).convert('RGB')
        tensor = self.transform(img).unsqueeze(0).to(self.device)
        with self.lock, torch.inference_mode():
            logits = self.model(tensor)
            if logits.shape != (1, len(self.labels)) or not torch.isfinite(logits).all():
                raise ValueError('花卉模型输出无效')
            scores, indices = logits.softmax(dim=1)[0].topk(min(5, len(self.labels)))
        results = []
        for score, index in zip(scores.tolist(), indices.tolist()):
            label = self.labels[index]
            results.append({
                'class': index, 'class_name': label['name'],
                'class_name_en': label['name_en'], 'confidence': float(score),
                'bbox': None, 'task': 'flower', 'model_id': self.model_id,
            })
        return results, img

    def detect(self, img_bytes):
        results, image = self._predict(img_bytes)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        text = ' / '.join(f"{r['class_name_en']} {r['confidence']:.1%}" for r in results[:3])
        draw.rectangle((0, 0, image.width, 28), fill=(22, 48, 35))
        draw.text((8, 8), text, font=font, fill='white')
        return results, image

    def detect_realtime(self, img_bytes, user_key=None):
        # Each frame uses the same preprocessing as uploaded images; no stale
        # prediction from a previous camera session is retained.
        results, _ = self._predict(img_bytes)
        return results, None, results[0]['confidence']
