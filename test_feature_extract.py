#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试单个 pcap 文件的特征提取
"""

import os
import sys

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), "TrafficFormer", "data_generation"))

from finetuning_data_gen import get_feature_flow

base_dir = os.path.dirname(os.path.abspath(__file__))
test_pcap = os.path.join(base_dir, "split_outputs/splitcap/aimchat/AIMchat1_TCP_10.pcap")

print("Testing pcap file:", test_pcap)
print("File exists:", os.path.exists(test_pcap))

if os.path.exists(test_pcap):
    try:
        result = get_feature_flow(
            test_pcap, 
            select_packet_len=64, 
            packets_num=5,
            start_index=28
        )
        print("\nResult type:", type(result))
        if result == -1:
            print("Feature extraction FAILED (returned -1)")
        else:
            print("Feature extraction SUCCESS!")
            print("Number of elements in result:", len(result))
    except Exception as e:
        print(f"Error during feature extraction: {e}")
        import traceback
        traceback.print_exc()
