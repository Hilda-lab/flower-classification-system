"""Evaluate the actual application service against a five-class ImageFolder test set."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from flower_classification_backend.backend.config import Config
from flower_classification_backend.backend.services.flower_service import FlowerService
from torchvision.datasets import ImageFolder


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('test_dir', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/flower-validation.json')
    args = parser.parse_args()
    model = FlowerService(Config.FLOWER_MODEL_DIR)
    dataset = ImageFolder(args.test_dir)
    expected = [label['name_en'] for label in model.labels]
    if dataset.classes != expected:
        raise ValueError(f'Test labels must match {expected}; got {dataset.classes}')
    matrix = [[0] * len(expected) for _ in expected]
    top3 = 0
    for path, label in dataset.samples:
        results, _, _ = model.detect_realtime(Path(path).read_bytes())
        matrix[label][results[0]['class']] += 1
        top3 += label in [r['class'] for r in results[:3]]
    correct = sum(matrix[i][i] for i in range(len(expected)))
    count = len(dataset)
    report = {
        'source': 'flower_photos held-out test split; not independent field evaluation',
        'model_id': model.model_id,
        'weight_sha256': hashlib.sha256((Path(Config.FLOWER_MODEL_DIR) / 'best-ckpt2.pt').read_bytes()).hexdigest(),
        'preprocessing': 'Application service: EXIF transpose, RGB, resize 224x224, normalize mean/std 0.5',
        'samples': count, 'correct': correct, 'top1_accuracy': correct / count,
        'top3_correct': top3, 'top3_accuracy': top3 / count,
        'classes': expected, 'confusion_matrix': matrix,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
