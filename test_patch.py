#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 flowcontainer 补丁
"""

import sys

# 先导入 flowcontainer.reader，然后修改它
import flowcontainer.reader
flowcontainer.reader.__tshark_max_version__ = '5.0.0'

# 然后导入 extract
from flowcontainer.extractor import extract

import os
base_dir = os.path.dirname(os.path.abspath(__file__))
test_pcap = os.path.join(base_dir, "split_outputs/splitcap/aimchat/AIMchat1_TCP_10.pcap")

print("Testing flowcontainer with patched version...")
print("Test pcap:", test_pcap)

try:
    result = extract(test_pcap, filter='tcp')
    print(f"Success! Number of flows extracted:", len(result))
    if result:
        first_key = list(result.keys())[0]
        print("First flow key:", first_key)
        print("First flow data:", result[first_key])
except Exception as e:
    print(f"Error:", e)
    import traceback
    traceback.print_exc()
