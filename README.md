# 5 类花卉识别系统

这是一个前后端分离的花卉图像识别平台，基于 ResNet18 模型实现 5 类花卉识别，提供用户、历史记录、统计和管理能力，并在首页提供花卉百科。

## 当前能力

- 上传图片、批量图片和摄像头实时识别
- 支持 5 类花卉：雏菊、蒲公英、玫瑰、向日葵、郁金香
- 返回 Top-3 候选、置信度和模型信息
- 用户注册、登录、识别历史、个人资料和管理员统计
- 首页花卉百科：中文名、英文名、简介、花期和养护提示
- SQLite 持久化用户、图片、识别历史和系统日志

## 目录

```text
flower_classification_backend/       Flask 后端（当前运行代码）
flower_classification_frontend/      Vue 3 + Vite 前端
model_assets/flower-resnet18/        五类标签和 best-ckpt2.pt 权重
scripts/download_flower_model.py     安装并校验自己训练的模型
docs/FLOWER_MODEL.md                 模型、接口和验证说明
requirements.txt                     完整识别功能依赖
requirements-preview.txt             无模型预览依赖
start-backend.ps1                    启动真实模型后端
start-preview.ps1                    启动无模型预览后端
start-frontend.ps1                   启动前端
```

## 启动

后端（PowerShell）：

```powershell
./start-backend.ps1
```

前端（另一个终端）：

```powershell
./start-frontend.ps1
```

浏览器访问 <http://127.0.0.1:3000>，前端会调用 `http://127.0.0.1:5001` 后端。

仓库包含当前使用的 `model_assets/flower-resnet18/best-ckpt2.pt`（约 44.79 MB），启动脚本会校验其 SHA256。克隆完整仓库后无需另行下载模型；仅在权重缺失时，使用 `scripts/download_flower_model.py --source <权重路径>` 安装，或配置 `FLOWER_MODEL_URL` 为该权重的 HTTPS 直链。其他权重、完整数据集、上传图片和 SQLite 数据库仍由 `.gitignore` 排除。

运行识别只需 `model_assets/flower-resnet18/` 中的 `best-ckpt2.pt` 和 `labels.json`，不需要完整数据集。`tests/fixtures/` 保留五类测试样例，`docs/training/` 保留训练与评估记录。

## 模型与验证

模型服务位于 `flower_classification_backend/backend/services/flower_service.py`，使用 ResNet18 和 224×224 图像预处理，输出 Top-3 候选。使用 flower_photos 数据集训练，在 550 张测试图片上的验证结果为 Top-1 90.36%、Top-3 98.91%；这只是该测试集上的结果，不等同于所有真实场景的准确率。

接口和字段说明见 [docs/FLOWER_MODEL.md](docs/FLOWER_MODEL.md)。

## 开发环境

- Python 3.10+，Flask、SQLAlchemy、PyTorch、torchvision、Pillow
- Node.js 18+，npm 8+
- Windows 可直接使用仓库中的 PowerShell 启动脚本

## 许可证

请遵循仓库中的 `LICENSE` 文件。
