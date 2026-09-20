# 五类花卉模型与接口说明

## 当前模型

- 自行训练的 ResNet18，ImageNet 预训练后全参数微调；分类头 512 → 5，总参数量 11,179,077。
- 权重：`model_assets/flower-resnet18/best-ckpt2.pt`，44,794,251 字节（42.72 MiB）。
- SHA256：`db18cc2e517fa7f008216164db8a7124856969739015072a00235d9ef3145b44`。
- 模型标识：`flower-resnet18-5class@2026-09-20`。
- 标签顺序：0 daisy / 雏菊、1 dandelion / 蒲公英、2 roses / 玫瑰、3 sunflowers / 向日葵、4 tulips / 郁金香。
- PyTorch `weights_only=True` 加载，严格匹配全部参数。运行时仅需此权重和五类标签文件。
- 输入：EXIF 方向纠正、RGB、Resize((224,224))、ToTensor、Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))。

## 训练与评估

数据为 flower_photos，共 3670 张，按类别约 70% / 15% / 15% 划分，随机种子 42：训练 2569、验证 551、测试 550。
Adam，学习率 0.0002，weight decay 0.0001，batch size 32，交叉熵损失，训练 12 轮。
增强包括颜色抖动、随机旋转、水平翻转和随机擦除。
第 11 轮最佳验证准确率 93.65%；测试 Top-1 为 497/550 = 90.36%，Top-3 为 544/550 = 98.91%。
训练记录及原始逐类指标保存在 `docs/training/`；应用服务复测结果保存在 `docs/flower-validation.json`。
这些结果不代表任意实际拍摄场景的准确率。

## 本地运行

```powershell
# 新环境：克隆仓库后，先创建 .venv 并安装 requirements.txt
# 仓库已包含 best-ckpt2.pt，启动时自动校验
.\start-backend.ps1
# 另一个终端
.\start-frontend.ps1
```

前端 http://127.0.0.1:3000，后端 http://127.0.0.1:5001。
`start-preview.ps1` 是不加载模型的页面预览。
`FLOWER_MODEL_DIR` 可指定包含新权重和五类 `labels.json` 的目录；`FLOWER_DEVICE` 默认 cpu，`FLOWER_NUM_THREADS` 默认 4。

## 部署

当前使用的 `best-ckpt2.pt` 纳入 Git，随代码一起提交和克隆；其他 `.pt` 文件继续忽略。
Render 构建执行 `scripts/render-build.sh`，直接校验仓库中的权重，不需要配置下载地址。
仅当权重文件缺失时，可用安装器的 `--source` 参数从本地恢复，或设置 `FLOWER_MODEL_URL` 为对应权重的 HTTPS 直链。文件必须通过上述 SHA256 校验；权重缺失且无可用来源或哈希不符时构建失败。

## 接口与历史

单图 `/api/detect`、批量 `/api/detect/batch`、实时 `/api/detect/realtime` 的响应结构不变。
结果包含 class、class_name、class_name_en、confidence、bbox=null、task=flower、model_id。
返回按概率排序的 Top-3 候选。概率仍由全部五类计算，不对前三项重新归一化，三项之和可能小于 100%。average_confidence 为第一候选概率，不是模型准确率。
新识别记录保存三个候选；已有历史记录保留原候选数量。五类标签、权重、Top-1 结果及模型标识不变。
历史记录保留原来的类别名称、索引和模型标识，不重新解释旧索引，不需要数据库改表。
管理后台识别总数包含所有历史记录；类别分布及平均信心度只统计当前 model_id，预览模式下这两项为空/0。

## 验证

```powershell
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/validate_flower_model.py "F:\BaiduNetdiskDownload\FlowerClassify\FlowerClassify\datasets\test"
npm.cmd --prefix flower_classification_frontend run build
```

集成测试使用 `tests/fixtures/` 中五张带署名的固定样例及临时数据库、上传目录，运行识别和集成测试不需要完整数据集。
这些样例是已正确分类的接口回归用例，不是准确率测试集。完整测试集评估使用上述独立命令。

## 限制

只能识别雏菊、蒲公英、玫瑰、向日葵、郁金香这五类花卉。
系统是整图分类，不提供多花定位或未知花种/非花拒识；其他图片也可能返回高置信度候选。
