# 项目审计与 GitHub 上传清单

## 当前运行链路

1. `flower_classification_backend/backend/app.py` 创建 Flask 应用并注册认证、检测、历史、统计和管理 API。
2. `flower_classification_backend/backend/services/flower_service.py` 加载 ResNet18 花卉权重，执行 224×224 预处理并返回 Top-5 结果。
3. 检测路由把图片交给模型服务，再由图片、历史和日志管理器写入 SQLite。
4. `flower_classification_frontend/src/router/index.js` 将 Vue 页面连接到后端接口；`HomePage.vue` 还提供 10 类花卉百科。
5. 数据库文件位于 `flower_classification_backend/backend/instance/garbage_classification.db`，属于本地运行数据，已被 Git 忽略。

## 应上传的核心内容

- Flask 后端源码、Vue 前端源码和启动脚本
- `model_assets/flower-resnet18/labels.json`
- `scripts/download_flower_model.py`
- `docs/FLOWER_INTEGRATION.md`、本审计文档和花卉百科配置
- `requirements-flower.txt`、`requirements-preview.txt`

## 不应上传的内容

- 模型权重 `*.pt`、测试数据压缩包和本地数据集
- `uploads/`、SQLite 数据库、日志、缓存、虚拟环境、`node_modules/`、前端 `dist/`
- 原垃圾分类训练配置 `garbage.yaml`、`classname.txt`、`garbage265_hierarchical/`
- 旧 YOLO 源码目录 `yolov5/`、`yolov5-6.2/`、旧脚本 `run_detect.sh`

这些条目已经写入根目录 `.gitignore`。本地文件暂时保留，便于回滚和对照；执行首次提交时不会进入 GitHub。

## 仍存在的历史命名

后端目录已迁移为 `flower_classification_backend/`，前端目录已迁移为 `flower_classification_frontend/`。数据库文件名暂时保留为 `garbage_classification.db`，因为它是本地 SQLite 数据文件，不会提交到 GitHub；改名需要额外的数据迁移，没有必要影响运行。

## 上传前检查

```powershell
git init
git add .
git status --short
```

确认状态中没有 `*.pt`、`datasets.zip`、`uploads/`、`*.db`、`yolov5/` 和垃圾分类配置后，再提交并推送。
