#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查生成的数据集
"""

import json
import os
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))

# 1. 检查 dataset.json
print("=== 检查 dataset.json ===")
with open(os.path.join(base_dir, "finetune_data/dataset.json"), "r") as f:
    dataset = json.load(f)

print("类别数:", len(dataset.keys()))
labels = {
    "0": "facebook_video",
    "1": "facebook_chat", 
    "2": "aimchat",
    "3": "email",
    "4": "facebook_audio"
}
for key in dataset.keys():
    print(f"类别 {key} ({labels[key]}): {dataset[key]['samples']} 个样本")

# 2. 检查 train_dataset.tsv
print("\n=== 检查 train_dataset.tsv ===")
train_df = pd.read_csv(os.path.join(base_dir, "finetune_data/dataset/train_dataset.tsv"), sep="\t")
print("训练集样本数:", len(train_df))
print("标签分布:")
print(train_df['label'].value_counts().sort_index())

# 3. 检查验证集
print("\n=== 检查 valid_dataset.tsv ===")
val_df = pd.read_csv(os.path.join(base_dir, "finetune_data/dataset/valid_dataset.tsv"), sep="\t")
print("验证集样本数:", len(val_df))
print("标签分布:")
print(val_df['label'].value_counts().sort_index())

# 4. 检查测试集
print("\n=== 检查 test_dataset.tsv ===")
test_df = pd.read_csv(os.path.join(base_dir, "finetune_data/dataset/test_dataset.tsv"), sep="\t")
print("测试集样本数:", len(test_df))
print("标签分布:")
print(test_df['label'].value_counts().sort_index())

print("\n✅ 数据集检查完成！格式正确！")
