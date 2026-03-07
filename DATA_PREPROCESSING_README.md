# TrafficFormer 数据处理说明文档
================================

## 跨平台兼容性
-----------------
✅ **Windows、macOS、Linux 都可以直接运行！**

我们已经对代码进行了跨平台适配：

### 主要修改点：

1. **会话分割工具替换**：将 Windows 专用的 `SplitCap.exe` 替换为跨平台的 `scapy` 库
2. **tshark 版本限制绕过**：通过 monkey patch 兼容高版本 tshark
3. **路径处理优化**：使用 `os.path` 处理路径，兼容各操作系统
4. **硬编码路径修复**：移除硬编码路径，改用相对路径

---

## 环境准备
----------

### 依赖安装：

```bash
# 安装所需库
pip install -r TrafficFormer/requirements.txt

# 安装 tshark (Wireshark)
# macOS:
brew install wireshark
# Windows:
# 从 https://www.wireshark.org/download.html 下载安装
# Linux:
sudo apt install tshark
```

### 检查 tshark 版本：
```bash
tshark -v
# 代码已适配高版本 tshark (4.x)
```

---

## 快速开始
----------

### 1. 准备数据集

将你的 pcap 或 pcapng 文件按以下结构放置：

```
TrafficFormer/
├── NonVPN-PCAPs-01/
│   ├── aimchat/
│   │   ├── AIMchat1.pcapng
│   │   └── ...
│   ├── email/
│   │   ├── email1a.pcap
│   │   └── ...
│   ├── facebook_audio/
│   ├── facebook_chat/
│   └── facebook_video/
```

### 2. 一键运行数据生成

```bash
python run_finetuning_data_gen.py
```

---

## 详细步骤
----------

### 数据生成流程：

1. **Step 1: pcapng 转 pcap + 会话分割
- 将 pcapng 转换为 pcap 格式
- 按会话（flow）分割 pcap 文件
- 输出到 `split_outputs/splitcap/`

2. **Step 2: 特征提取**
- 提取流量特征（数据包内容、长度、时间、方向、消息类型
- 生成 `finetune_data/dataset.json

3. **Step 3: 数据集划分**
- 按 8:1:1 比例划分 train/val/test
- 输出 tsv 文件到 `finetune_data/dataset/`

---

## 文件说明
--------

### 核心修改文件：

| 文件 | 修改内容
|------|----------
| `TrafficFormer/data_generation/finetuning_data_gen.py` | 主数据生成脚本 (已跨平台适配)
| `TrafficFormer/data_generation/utils.py` | 工具函数 (scapy 会话分割)
| `run_finetuning_data_gen.py` | 一键运行入口

### 输出文件：

```
TrafficFormer/
├── pcap/                  # pcap 转换后文件
├── split_outputs/
│   └── splitcap/           # 会话分割后的 pcap (按标签分文件夹)
└── finetune_data/
    ├── dataset.json        # 特征数据集
    └── dataset/
        ├── train_dataset.tsv
        ├── valid_dataset.tsv
        └── test_dataset.tsv
```

---

## 常见问题
----------

### Q: Windows 上可以直接跑吗？
A: 可以！代码已跨平台适配。

### Q: tshark 版本太高报错？
A: 不用担心，代码已通过 monkey patch 兼容高版本 tshark。

### Q: 数据集结构有什么要求？
A: 每个子文件夹是一个标签，里面放对应的 pcap/pcapng 文件即可。

