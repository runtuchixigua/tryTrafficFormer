#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrafficFormer 微调数据生成脚本（适配 macOS）
已修改：使用 scapy 替代 SplitCap.exe 来分割 pcap 文件
"""

if __name__ == "__main__":
    print("========== Finetuning Data Generation ==========\n")

    import os
    import sys

    # 添加项目路径
    sys.path.append(os.path.join(os.path.dirname(__file__), "TrafficFormer", "data_generation"))

    from finetuning_data_gen import convert_splitcap, generation_multiP, dataset_extract

    # ==================================================
    # 1️⃣ 固定路径（已配置好）
    # ==================================================
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pcapng_path = os.path.join(base_dir, "NonVPN-PCAPs-01/")  # 原始数据路径
    pcap_path = os.path.join(base_dir, "pcap/")                  # pcap 转换后的保存路径
    pcap_split_path = os.path.join(base_dir, "split_outputs/")   # 分割后的 pcap 保存路径
    dataset_save_path = os.path.join(base_dir, "finetune_data/") # 最终数据集保存路径

    os.makedirs(pcap_path, exist_ok=True)
    os.makedirs(pcap_split_path, exist_ok=True)
    os.makedirs(dataset_save_path, exist_ok=True)

    # ==================================================
    # Step 1: Split PCAP
    # 每个 pcap 是一个 class
    # ==================================================
    print("Step 1: Convert & Split PCAP")

    convert_splitcap(
        pcapng_path=pcapng_path,
        pcap_path=pcap_path,
        pcap_split_path=pcap_split_path,
        is_pcap_label=True     # ⚠ 按要求必须 True
    )

    # ==================================================
    # Step 2: Generate dataset.json
    # ==================================================
    print("\nStep 2: Generate dataset.json")

    splitcap_dir = os.path.join(pcap_split_path, "splitcap/")

    label_dirs = [
        d for d in os.listdir(splitcap_dir)
        if os.path.isdir(os.path.join(splitcap_dir, d))
    ]

    category_num = len(label_dirs)
    print("Category number:", category_num)

    samples_per_class = 300
    samples = [samples_per_class] * category_num

    generation_multiP(
        pcap_path=splitcap_dir,
        samples=samples,
        dataset_save_path=dataset_save_path,
        payload_length=64,
        payload_packet=5,
        start_index=28      # ⚠ finetune 必须 28（从IP头开始）
    )

    # ==================================================
    # Step 3: dataset.json → train/val/test.tsv
    # ==================================================
    print("\nStep 3: Generate train/valid/test TSV")

    dataset_extract(
        dataset_save_path=dataset_save_path,
        pcap_path=splitcap_dir,
        features=['datagram', "length", "time", "direction", "message_type"],
        dataset_level="flow"     # ⚠ flow级别
    )

    print("\n========== FINISHED ==========")
    print("Check dataset in:", os.path.join(dataset_save_path, "dataset/"))
