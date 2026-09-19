# 花卉模型与接口说明

## 模型

系统使用本地部署的 ResNet18 花卉分类模型，完全本机推理，不调用任何外部识别 API。
支持风铃草、康乃馨、雏菊、蒲公英、薰衣草、百合、荷花、玫瑰、向日葵、郁金香。

- 后端提供单图 `/api/detect`、批量 `/api/detect/batch`、实时 `/api/detect/realtime` 接口，以及 JWT 鉴权、数据库、上传和历史记录。
- 结果包含 class / class_name / confidence / bbox，以及 task=flower、model_id、class_name_en。bbox 为 null：这是整图分类，不定位多个花朵。
- 上传结果的 average_confidence 为 Top-1，与实时、历史页面、后台口径一致。
- 后台类别分布只统计当前花卉模型产生的记录。
- Vue 前端使用 3000 端口，5001 是 API 服务；运行产物（模型权重、上传图片、数据库）通过 Git 忽略规则排除，不进入仓库。

## 运行

在项目根目录打开两个 PowerShell 终端：

```powershell
# 终端 1：已加载花卉模型的后端
.\start-backend.ps1
# 终端 2：前端
.\start-frontend.ps1
```

访问 http://127.0.0.1:3000 。
不要用 start-preview.ps1 启动真实识别：该脚本用于不加载模型的页面预览。
若已有后端进程占用 5001 端口，请先在它的终端按 Ctrl+C。

新环境：创建 `.venv`，安装 `requirements.txt`，前端安装 package-lock.json 对应依赖。
若权重缺失，在根目录执行：

```powershell
.\.venv\Scripts\python.exe scripts/download_flower_model.py
# 可选：下载测试数据集（运行识别不需要数据集）
.\.venv\Scripts\python.exe scripts/download_flower_model.py --test-data
```

模型约 44.8 MB。环境变量 FLOWER_MODEL_DIR 可调整资产目录；FLOWER_DEVICE 默认 cpu，FLOWER_NUM_THREADS 默认 4。

## 模型文件与预处理

- 权重 `best-ckpt1.pt` 与测试集压缩包在下载时按 SHA256 自动校验，校验值固定在 `scripts/download_flower_model.py` 中。
- 权重通过 torch.load(weights_only=True) 加载，与本地 torchvision ResNet18 严格匹配全部参数。
- 标签按字典序 Bellflower ... Tulip 排列，`model_assets/flower-resnet18/labels.json` 保存索引与中文名称。
- 预处理：RGB、Resize((224,224))、ToTensor、均值和标准差均为 (0.5,0.5,0.5)，并纠正 EXIF 方向；上传与实时识别保持一致。

## 验证结果

本机 Python 3.10、PyTorch 2.8.0+cpu、torchvision 0.23.0+cpu。

- 全部模型参数严格加载成功，真实输入得到 10 类输出。
- 测试集每类按文件名排序取前 10 张，共 100 张，Top-1 正确 96 张。康乃馨 8/10，玫瑰与郁金香各 9/10，其余各 10/10。
- 明细见 flower-validation.json。这是固定小样本检查，不是完整测试集成绩，也不是独立实际拍摄准确率。
- tests/test_flower_integration.py：真实模型通过单图、结果图、历史、类别统计、批量部分失败、实时一致性、鉴权、格式拒绝和预览模式检查。测试使用临时 SQLite 与临时 uploads，不污染业务数据。
- 前端 npm run build 通过。
- docs/sample-flowers 保存三张示例图片，供本地上传体验。

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_flower_integration.py -v
npm.cmd --prefix flower_classification_frontend run build
```

## 使用限制

只支持上述 10 个类别，始终返回前 5 个候选；低置信度或非花图片也可能给出错误甚至高置信度答案，结果仅供参考，不具备未知花种/非花拒识能力。
