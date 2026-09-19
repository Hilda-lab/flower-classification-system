# 10 类花卉识别系统

这是一个前后端分离的花卉图像识别平台，基于 ResNet18 模型实现 10 类花卉识别，提供用户、历史记录、统计和管理能力，并在首页提供花卉百科。

## 当前能力

- 上传图片、批量图片和摄像头实时识别
- 支持 10 类花卉：风铃草、康乃馨、雏菊、蒲公英、薰衣草、百合、荷花、玫瑰、向日葵、郁金香
- 返回 Top-5 候选、置信度和模型信息
- 用户注册、登录、识别历史、个人资料和管理员统计
- 首页花卉百科：中文名、英文名、简介、花期和养护提示
- SQLite 持久化用户、图片、识别历史和系统日志

## 目录

```text
flower_classification_backend/       Flask 后端（当前运行代码）
flower_classification_frontend/      Vue 3 + Vite 前端
model_assets/flower-resnet18/        模型标签和本地权重缓存
scripts/download_flower_model.py     下载并校验模型/测试数据
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

首次运行没有模型文件时，后端会根据 `model_assets/flower-resnet18/labels.json` 和下载脚本准备权重。模型权重、数据集压缩包、上传图片和 SQLite 数据库均不应提交到 GitHub，具体见 `.gitignore`。

## 模型与验证

模型服务位于 `flower_classification_backend/backend/services/flower_service.py`，使用 ResNet18 和 224×224 图像预处理，输出 Top-5 候选。在 556 张测试图片上的验证结果为 Top-1 97.30%、Top-5 100%；这只是该测试集上的结果，不等同于所有真实场景的准确率。

接口和字段说明见 [docs/FLOWER_MODEL.md](docs/FLOWER_MODEL.md)。

## 开发环境

- Python 3.10+，Flask、SQLAlchemy、PyTorch、torchvision、Pillow
- Node.js 18+，npm 8+
- Windows 可直接使用仓库中的 PowerShell 启动脚本

## 许可证

请遵循仓库中的 `LICENSE` 文件。
