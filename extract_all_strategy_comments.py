#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from pathlib import Path

def extract_strategy_comments_from_text(text):
    """从文本中提取strategy comments部分"""
    # 查找 [STRATEGY COMMENTS] 部分
    strategy_pattern = r'\[STRATEGY COMMENTS\]\s*\n(.*?)(?=\n\[|$)'
    match = re.search(strategy_pattern, text, re.DOTALL | re.IGNORECASE)
    
    if match:
        strategy_content = match.group(1).strip()
        # 移除文本中的strategy comments部分
        remaining_text = re.sub(strategy_pattern, '', text, flags=re.DOTALL | re.IGNORECASE).strip()
        return strategy_content, remaining_text
    
    return None, text

def process_all_translation_pairs():
    """处理所有翻译对，分离strategy comments"""
    
    # 读取原始文件
    with open('ml_translation_pairs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pairs = data['pairs']
    new_pairs = []
    strategy_pairs = []
    pair_counter = 1
    
    # 清理individual_pairs目录
    individual_dir = Path('individual_pairs')
    if individual_dir.exists():
        for file in individual_dir.glob('*.json'):
            file.unlink()
    else:
        individual_dir.mkdir(exist_ok=True)
    
    for pair in pairs:
        english_text = pair['english']
        chinese_text = pair['chinese']
        
        # 从英文文本中提取strategy comments
        eng_strategy, eng_remaining = extract_strategy_comments_from_text(english_text)
        
        # 从中文文本中提取strategy comments
        chi_strategy, chi_remaining = extract_strategy_comments_from_text(chinese_text)
        
        # 如果找到strategy comments，创建独立的翻译对
        if eng_strategy and chi_strategy:
            strategy_pair = {
                'english': eng_strategy,
                'chinese': chi_strategy,
                'section_type': 'STRATEGY_COMMENTS',
                'source_file': pair['source_file'],
                'confidence': pair['confidence']
            }
            strategy_pairs.append(strategy_pair)
            
            # 创建strategy comments的单独文件
            strategy_filename = f"pair_{pair_counter:03d}_{pair['source_file'].replace(' ', '_').replace('[', '__').replace(']', '__')}_strategy_comments.json"
            strategy_file_data = {
                'id': f'pair_{pair_counter:03d}',
                **strategy_pair
            }
            
            with open(f'individual_pairs/{strategy_filename}', 'w', encoding='utf-8') as f:
                json.dump(strategy_file_data, f, ensure_ascii=False, indent=2)
            
            pair_counter += 1
            
            # 更新原始翻译对，移除strategy comments
            updated_pair = {
                **pair,
                'english': eng_remaining,
                'chinese': chi_remaining
            }
            new_pairs.append(updated_pair)
        else:
            # 没有strategy comments，保持原样
            new_pairs.append(pair)
        
        # 为每个翻译对创建单独文件
        filename = f"pair_{pair_counter:03d}_{pair['source_file'].replace(' ', '_').replace('[', '__').replace(']', '__')}.json"
        file_data = {
            'id': f'pair_{pair_counter:03d}',
            **new_pairs[-1]
        }
        
        with open(f'individual_pairs/{filename}', 'w', encoding='utf-8') as f:
            json.dump(file_data, f, ensure_ascii=False, indent=2)
        
        pair_counter += 1
    
    # 添加strategy comments翻译对到主列表
    all_pairs = new_pairs + strategy_pairs
    
    # 更新元数据
    data['metadata']['total_pairs'] = len(all_pairs)
    data['metadata']['extraction_stats']['total_pairs'] = len(all_pairs)
    if 'strategy_comments_pairs' not in data['metadata']['extraction_stats']:
        data['metadata']['extraction_stats']['strategy_comments_pairs'] = 0
    data['metadata']['extraction_stats']['strategy_comments_pairs'] = len(strategy_pairs)
    data['pairs'] = all_pairs
    
    # 保存更新后的文件
    with open('ml_translation_pairs.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"处理完成！")
    print(f"总翻译对数: {len(all_pairs)}")
    print(f"Strategy comments翻译对数: {len(strategy_pairs)}")
    print(f"创建的单独文件数: {pair_counter - 1}")

if __name__ == '__main__':
    process_all_translation_pairs()