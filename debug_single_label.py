#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本 - 只处理单个标签文件夹
"""

if __name__ == "__main__":
    print("========== Debug Single Label Generation ==========\n")

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
    pcap_path = os.path.join(base_dir, "pcap_debug/")            # pcap 转换后的保存路径
    pcap_split_path = os.path.join(base_dir, "split_outputs_debug/")  # 分割后的 pcap 保存路径
    dataset_save_path = os.path.join(base_dir, "finetune_data_debug/")  # 最终数据集保存路径

    # 清理旧目录
    import shutil
    if os.path.exists(pcap_path):
        shutil.rmtree(pcap_path)
    if os.path.exists(pcap_split_path):
        shutil.rmtree(pcap_split_path)
    if os.path.exists(dataset_save_path):
        shutil.rmtree(dataset_save_path)
    if os.path.exists("./temp/"):
        shutil.rmtree("./temp/")

    os.makedirs(pcap_path, exist_ok=True)
    os.makedirs(pcap_split_path, exist_ok=True)
    os.makedirs(dataset_save_path, exist_ok=True)
    os.makedirs("./temp/", exist_ok=True)

    # ==================================================
    # Step 1: 只处理单个标签文件夹 (aimchat)
    # ==================================================
    print("Step 1: Convert & Split Single Label (aimchat)")

    # 修改 convert_splitcap 只处理单个标签
    import tempfile
    import shutil

    # 创建临时目录，只包含 aimchat
    temp_pcapng = os.path.join(base_dir, "temp_pcapng_aimchat")
    shutil.copytree(os.path.join(pcapng_path, "aimchat"), os.path.join(temp_pcapng, "aimchat"))

    convert_splitcap(
        pcapng_path=temp_pcapng,
        pcap_path=pcap_path,
        pcap_split_path=pcap_split_path,
        is_pcap_label=True
    )

    # 清理临时目录
    shutil.rmtree(temp_pcapng)

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
    print("Labels found:", label_dirs)

    samples_per_class = 300
    samples = [samples_per_class] * category_num

    generation_multiP(
        pcap_path=splitcap_dir,
        samples=samples,
        dataset_save_path=dataset_save_path,
        payload_length=64,
        payload_packet=5,
        start_index=28
    )

    # ==================================================
    # Step 3: dataset.json → train/val/test.tsv
    # ==================================================
    print("\nStep 3: Generate train/valid/test TSV")

    dataset_extract(
        dataset_save_path=dataset_save_path,
        pcap_path=splitcap_dir,
        features=['datagram', "length", "time", "direction", "message_type"],
        dataset_level="flow"
    )

    print("\n========== FINISHED ==========")
