import os
import sys
sys.path.append(os.getcwd())
import random
import binascii
import scapy.all as scapy
import json
from tqdm import tqdm
import pandas as pd
from sklearn.model_selection import train_test_split
from collections import defaultdict

def get_label_from_filename(filename):
    filename_lower = filename.lower()
    if 'aim' in filename_lower:
        return 'aim_chat'
    elif 'email' in filename_lower:
        return 'email'
    elif 'facebook_audio' in filename_lower or 'facebookaudio' in filename_lower:
        return 'facebook_audio'
    elif 'facebook_video' in filename_lower or 'facebookvideo' in filename_lower:
        return 'facebook_video'
    elif 'facebook_chat' in filename_lower or 'facebookchat' in filename_lower:
        return 'facebook_chat'
    else:
        return 'unknown'

def get_flow_key(packet):
    if scapy.IP in packet:
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        proto = packet[scapy.IP].proto
    elif scapy.IPv6 in packet:
        src_ip = packet[scapy.IPv6].src
        dst_ip = packet[scapy.IPv6].dst
        proto = packet[scapy.IPv6].nh
    else:
        return None
    
    src_port = 0
    dst_port = 0
    if scapy.TCP in packet:
        src_port = packet[scapy.TCP].sport
        dst_port = packet[scapy.TCP].dport
    elif scapy.UDP in packet:
        src_port = packet[scapy.UDP].sport
        dst_port = packet[scapy.UDP].dport
    
    forward_key = (src_ip, dst_ip, src_port, dst_port, proto)
    backward_key = (dst_ip, src_ip, dst_port, src_port, proto)
    
    return forward_key, backward_key

def extract_flows_from_pcap(pcap_file, max_flows=100):
    try:
        packets = scapy.rdpcap(pcap_file)
    except Exception as e:
        print(f"Error reading {pcap_file}: {e}")
        return []
    
    flows = defaultdict(list)
    
    for packet in packets:
        result = get_flow_key(packet)
        if result is None:
            continue
        
        forward_key, backward_key = result
        
        if forward_key in flows:
            flows[forward_key].append(packet)
        elif backward_key in flows:
            flows[backward_key].append(packet)
        else:
            flows[forward_key].append(packet)
    
    flow_list = []
    for key, packets in flows.items():
        if len(packets) >= 3:
            flow_list.append((key, packets))
    
    random.shuffle(flow_list)
    return flow_list[:max_flows]

def flow_feature_extract(packets, src_ip, payload_length=64, payload_packet=5, start_index=28):
    datagrams = []
    
    for i, packet in enumerate(packets[:payload_packet]):
        try:
            if scapy.IP in packet:
                packet_bytes = bytes(packet[scapy.IP])
            elif scapy.IPv6 in packet:
                packet_bytes = bytes(packet[scapy.IPv6])
            else:
                continue
            
            hex_str = binascii.hexlify(packet_bytes).decode()
            hex_str = hex_str[start_index * 2:]
            
            if len(hex_str) < payload_length * 2:
                hex_str = hex_str + '0' * (payload_length * 2 - len(hex_str))
            else:
                hex_str = hex_str[:payload_length * 2]
            
            datagrams.append(hex_str)
        except Exception as e:
            continue
    
    if len(datagrams) > 0:
        return '[SEP]' + '[SEP]'.join(datagrams)
    else:
        return None

def process_pcap_file(pcap_file, label, label_id, max_flows=50):
    flows_data = []
    
    flow_list = extract_flows_from_pcap(pcap_file, max_flows)
    
    for key, packets in flow_list:
        src_ip = key[0]
        datagram = flow_feature_extract(packets, src_ip)
        
        if datagram:
            flows_data.append({
                'datagram': datagram,
                'label': label_id[label]
            })
    
    return flows_data

def generate_dataset(pcap_path, output_path, samples_per_class=500):
    os.makedirs(output_path, exist_ok=True)
    
    print("Scanning pcap files...")
    pcap_files = []
    for file in os.listdir(pcap_path):
        if file.endswith('.pcap') or file.endswith('.pcapng'):
            label = get_label_from_filename(file)
            if label != 'unknown':
                pcap_files.append((os.path.join(pcap_path, file), label))
    
    print(f"Found {len(pcap_files)} pcap files")
    
    labels = sorted(set([label for _, label in pcap_files]))
    label_id = {name: idx for idx, name in enumerate(labels)}
    
    print(f"\nLabels ({len(labels)} classes):")
    for key in label_id.keys():
        print(f"  {key}: {label_id[key]}")
    
    print("\nProcessing pcap files...")
    all_data = []
    
    for label in labels:
        label_files = [(f, l) for f, l in pcap_files if l == label]
        flows_per_file = max(1, samples_per_class // len(label_files))
        
        print(f"\nProcessing {label} ({len(label_files)} files, ~{flows_per_file} flows/file)...")
        
        for pcap_file, _ in tqdm(label_files):
            flows_data = process_pcap_file(pcap_file, label, label_id, max_flows=flows_per_file)
            all_data.extend(flows_data)
    
    print(f"\nTotal samples collected: {len(all_data)}")
    
    if len(all_data) == 0:
        print("No data collected! Please check your pcap files.")
        return None
    
    data = pd.DataFrame(all_data)
    
    print("\nSamples per class:")
    print(data['label'].value_counts())
    
    print("\nSplitting dataset...")
    data_train, data_test = train_test_split(data, test_size=0.2, random_state=41, stratify=data["label"])
    data_val, data_test = train_test_split(data_test, test_size=0.5, random_state=42, stratify=data_test["label"])
    
    print(f"Train: {len(data_train)}, Val: {len(data_val)}, Test: {len(data_test)}")
    
    def write_tsv(data_df, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("label\ttext_a\n")
            for idx, row in data_df.iterrows():
                f.write(f"{row['label']}\t{row['datagram']}\n")
    
    write_tsv(data_train, os.path.join(output_path, "train_dataset.tsv"))
    write_tsv(data_val, os.path.join(output_path, "valid_dataset.tsv"))
    write_tsv(data_test, os.path.join(output_path, "test_dataset.tsv"))
    
    with open(os.path.join(output_path, "label_mapping.json"), "w") as f:
        json.dump(label_id, f, indent=2)
    
    print(f"\nDataset saved to {output_path}")
    return label_id

if __name__ == "__main__":
    pcap_path = "/Users/cherry/Documents/外k/TrafficFormer/NonVPN-PCAPs-01"
    output_path = "/Users/cherry/Documents/外k/TrafficFormer/TrafficFormer/dataset"
    
    print("=" * 60)
    print("TrafficFormer Dataset Generation")
    print("=" * 60)
    
    label_id = generate_dataset(pcap_path, output_path, samples_per_class=500)
    
    print("\n" + "=" * 60)
    print("Dataset generation completed!")
    print("=" * 60)
