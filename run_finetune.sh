#!/bin/bash

source /opt/homebrew/anaconda3/etc/profile.d/conda.sh
conda activate trafficformer

cd /Users/cherry/Documents/外k/TrafficFormer/TrafficFormer

python fine-tuning/run_classifier.py \
    --vocab_path models/encryptd_vocab.txt \
    --train_path /Users/cherry/Documents/外k/TrafficFormer/finetune_data/dataset/train_dataset.tsv \
    --dev_path /Users/cherry/Documents/外k/TrafficFormer/finetune_data/dataset/valid_dataset.tsv \
    --test_path /Users/cherry/Documents/外k/TrafficFormer/finetune_data/dataset/test_dataset.tsv \
    --pretrained_model_path /Users/cherry/Documents/外k/TrafficFormer/nomoe_bertflow_pre-trained_model.bin-120000 \
    --output_model_path /Users/cherry/Documents/外k/TrafficFormer/finetuned_model.bin \
    --config_path models/bert/base_config.json \
    --epochs_num 4 \
    --earlystop 4 \
    --batch_size 32 \
    --embedding word_pos_seg \
    --encoder transformer \
    --mask fully_visible \
    --seq_length 320 \
    --learning_rate 6e-5 \
    --pooling first \
    --tokenizer space
