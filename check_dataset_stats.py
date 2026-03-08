import json
import csv
from collections import Counter

def check_dataset():
    dataset_path = "/Users/cherry/Documents/外k/TrafficFormer/finetune_data"
    
    # 读取dataset.json
    with open(f"{dataset_path}/dataset.json", "r") as f:
        dataset_json = json.load(f)
    
    print("=== 数据集JSON信息 ===")
    print(f"类别数量: {len(dataset_json.keys())}")
    total_samples = 0
    for label_id, data in dataset_json.items():
        print(f"类别 {label_id}: {data['samples']} 个样本")
        total_samples += data['samples']
    print(f"总样本数: {total_samples}")
    
    # 读取tsv文件
    splits = ['train', 'valid', 'test']
    label_names = {
        '0': 'facebook_video',
        '1': 'facebook_audio', 
        '2': 'aimchat',
        '3': 'facebook_chat',
        '4': 'email'
    }
    
    print("\n=== TSV数据集信息 ===")
    all_labels = []
    for split in splits:
        tsv_path = f"{dataset_path}/dataset/{split}_dataset.tsv"
        labels = []
        with open(tsv_path, "r") as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                labels.append(row['label'])
                all_labels.append(row['label'])
        
        label_dist = Counter(labels)
        print(f"\n{split.capitalize()}数据集:")
        print(f"样本数: {len(labels)}")
        for label_id, count in sorted(label_dist.items()):
            print(f"  {label_names[label_id]} ({label_id}): {count}")
    
    print("\n=== 整体标签分布 ===")
    total_label_dist = Counter(all_labels)
    for label_id, count in sorted(total_label_dist.items()):
        print(f"{label_names[label_id]} ({label_id}): {count}")

if __name__ == "__main__":
    check_dataset()
