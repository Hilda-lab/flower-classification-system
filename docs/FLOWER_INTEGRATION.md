# 花卉模型接入记录（2026-09-19）

## 已完成

当前默认使用 LIU42/FlowerClassify v1.4.0 已训练的 ResNet18，完全本地推理，没有重新训练，没有调用收费识别 API。
支持风铃草、康乃馨、雏菊、蒲公英、薰衣草、百合、荷花、玫瑰、向日葵、郁金香。

保持原 Flask 单图 `/api/detect`、批量 `/api/detect/batch`、实时 `/api/detect/realtime` 接口以及原有 JWT 鉴权、数据库、上传和历史记录。
结果保留 class / class_name / confidence / bbox，并增加 task=flower、model_id、class_name_en。bbox 为 null：这是整图分类，不定位多个花朵。
上传结果的 average_confidence 为 Top-1，与实时、历史页面、后台口径一致；保留字段名以兼容原前端。
历史数据库表结构保持兼容，但后台类别分布只统计当前花卉模型记录。
前端沿用原页面框架与样式，替换识别标签、主题文案、主页指南和图标；回收地图入口移除，旧地址转到关于页。
旧 YOLO 训练目录和运行产物已加入 Git 忽略规则；使用 Vue 前端 3000 端口，5001 是 API 服务。

## 运行

在项目根目录打开两个 PowerShell 终端：

```powershell
# 终端 1：已加载花卉模型的后端
.\start-flower.ps1
# 终端 2：前端
.\start-frontend.ps1
```

访问 http://127.0.0.1:3000 。已有账号和数据库继续使用。
不要用 start-preview.ps1 启动真实识别：该脚本仍用于不加载模型的页面预览。
若已有旧后端占用 5001，请先在它的终端按 Ctrl+C。

新环境：创建 `.venv`，安装 `requirements-flower.txt`，前端安装 package-lock.json 对应依赖。
若权重缺失，在根目录执行：

```powershell
.\.venv\Scripts\python.exe scripts/download_flower_model.py
# 可选：下载作者数据供测试（运行识别不需要数据集）
.\.venv\Scripts\python.exe scripts/download_flower_model.py --test-data
```

模型约 44.8 MB。环境变量 FLOWER_MODEL_DIR 可调整资产目录；FLOWER_DEVICE 默认 cpu，FLOWER_NUM_THREADS 默认 4。

## 来源与可复现配置

- GitHub：https://github.com/LIU42/FlowerClassify
- 代码核查 revision：fef1144afb2c2ca44831555908a570bf15a035c9
- 权重及数据：https://github.com/LIU42/FlowerClassify/releases/tag/v1.4.0
- best-ckpt1.pt SHA256：be70e44fae334d14d4485d6fb49cb9b31637ebcdc2156b32da78678bd605d0f1
- datasets.zip SHA256：6804192695a6211c9fad1f3024c29ed9666d0e9115e0ccd310b67c1a46ceddf0
- 权重通过 torch.load(weights_only=True) 加载；用本地 torchvision ResNet18 严格匹配全部参数。不执行下载项目的 Python 文件。
- 作者 train.py 使用 ImageFolder；已核查数据包 train / valid / test 的目录一致，标签按字典序 Bellflower ... Tulip 排列。labels.json 保存此索引与中文名称。
- 推理沿用作者验证变换：RGB、Resize((224,224))、ToTensor、均值和标准差均为 (0.5,0.5,0.5)。作者 ONNX 服务另外采用中心裁剪；本接入明确选择其 PyTorch 验证流程，上传与实时保持一致，并纠正 EXIF 方向。
- 不沿用原垃圾模型的 448 输入、ImageNet 标准化、特殊数字标签重排和跨帧概率缓存。

## 验证结果

本机 Python 3.10、PyTorch 2.8.0+cpu、torchvision 0.23.0+cpu。

- 全部模型参数严格加载成功，真实输入得到 10 类输出。
- 从作者 datasets/test 每类按文件名排序取前 10 张，共 100 张，Top-1 正确 96 张。康乃馨 8/10，玫瑰与郁金香各 9/10，其余各 10/10。
- 明细见 flower-validation.json。这是作者测试数据上的固定小样本接入检查，不是完整测试集成绩，也不是独立实际拍摄准确率。
- tests/test_flower_integration.py：真实模型通过单图、结果图、历史、类别统计、批量部分失败、实时一致性、鉴权、格式拒绝和预览模式检查。测试使用临时 SQLite 与临时 uploads，不污染现有业务数据。
- 前端 npm run build 通过。浏览器检查了花卉首页、现有管理员账号登录和识别页面上传入口；未启用实际摄像头，实时后端用图片帧验证。
- docs/sample-flowers 保存作者测试集中的三张示例，供本地上传体验，来源及使用条件同作者数据。

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_flower_integration.py -v
npm.cmd --prefix flower_classification_frontend run build
```

## 限制与授权

只支持上述 10 个类别，始终返回前 5 个候选；低置信度或非花图片也可能给出错误甚至高置信度答案。不声称具备未知花种/非花拒识能力。
没有重新训练，不应把原作者模型训练成果归为本项目自主训练结果。
截至核查时，上游仓库未提供明确 LICENSE，数据描述为整理自多个 Kaggle 数据集。公开可下载不等同于允许再分发或商用；此接入用于当前本地验证，发布前需确认权重、源码、数据各自授权。
已保留修改前主要源文件备份 `.cache/before-flower-integration/`；现有 SQLite 数据库没有重建或清空。
