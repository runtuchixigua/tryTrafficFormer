#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 tshark 输出
"""

import os
import subprocess
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
test_pcap = os.path.join(base_dir, "split_outputs/splitcap/aimchat/AIMchat1_TCP_10.pcap")

print("Testing tshark with:", test_pcap)

# 尝试各种 tshark 命令
cmd1 = f"tshark -r {test_pcap} -T json"
print("\n=== 命令1: tshark -r <file> -T json ===")
try:
    result = subprocess.run(cmd1, shell=True, capture_output=True, text=True, timeout=30)
    print("Exit code:", result.returncode)
    if result.stdout:
        print("\n前1000字符输出:\n", result.stdout[:1000])
except Exception as e:
    print("Error:", e)

# 尝试 flowcontainer 可能使用的参数
cmd2 = f"tshark -r {test_pcap} -T fields -e frame.time_epoch -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e ip.len -e frame.number"
print("\n=== 命令2: 提取基本字段 ===")
try:
    result = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=30)
    print("Exit code:", result.returncode)
    if result.stdout:
        print("\n输出:\n", result.stdout)
except Exception as e:
    print("Error:", e)

# 检查 tshark 版本
print("\n=== tshark 版本 ===")
subprocess.run("tshark -v", shell=True)
