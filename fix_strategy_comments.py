#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import os
from pathlib import Path

def extract_strategy_comments_from_file(file_path):
    """从原始文件中提取strategy comments部分"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找strategy comments部分
        strategy_pattern = r'\[STRATEGY COMMENTS\]\s*([\s\S]*?)(?=\[SET CREDITS\]|$)'
        strategy_match = re.search(strategy_pattern, content)
        
        if strategy_match:
            strategy_content = strategy_match.group(1).strip()
            return strategy_content
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def find_chinese_strategy_comments(content):
    """从中文内容中提取strategy comments部分"""
    # 查找中文的strategy comments
    chinese_strategy_pattern = r'Other Options\s*====([\s\S]*?)Checks and Counters\s*====([\s\S]*?)$'
    match = re.search(chinese_strategy_pattern, content)
    
    if match:
        other_options = match.group(1).strip()
        checks_counters = match.group(2).strip()
        
        # 移除credits部分
        credits_pattern = r'\[CREDITS\][\s\S]*$'
        checks_counters = re.sub(credits_pattern, '', checks_counters).strip()
        
        return f"Other Options\n====\n{other_options}\nChecks and Counters\n====\n{checks_counters}"
    return None

def process_translation_pairs():
    """处理翻译对，提取并分离strategy comments"""
    
    # 读取当前的翻译对文件
    with open('ml_translation_pairs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_pairs = []
    strategy_pairs_count = 0
    
    for pair in data['translation_pairs']:
        # 保留原有的翻译对
        new_pairs.append(pair)
        
        # 检查是否包含strategy comments
        if '[STRATEGY COMMENTS]' in pair['english']:
            # 从英文中提取strategy comments
            english_content = pair['english']
            strategy_start = english_content.find('[STRATEGY COMMENTS]')
            
            if strategy_start != -1:
                english_strategy = english_content[strategy_start:].replace('[STRATEGY COMMENTS]\n', '').strip()
                
                # 从中文中提取对应的strategy comments
                chinese_strategy = find_chinese_strategy_comments(pair['chinese'])
                
                if chinese_strategy:
                    # 创建新的strategy comments翻译对
                    strategy_pair = {
                        "english": english_strategy,
                        "chinese": chinese_strategy,
                        "section_type": "STRATEGY_COMMENTS",
                        "source_file": pair['source_file'],
                        "confidence": 1.0
                    }
                    new_pairs.append(strategy_pair)
                    strategy_pairs_count += 1
                    
                    # 从原翻译对中移除strategy comments
                    pair['english'] = english_content[:strategy_start].strip()
                    
                    # 从中文中移除strategy comments部分
                    chinese_without_strategy = re.sub(r'Other Options\s*====[\s\S]*$', '', pair['chinese']).strip()
                    pair['chinese'] = chinese_without_strategy
    
    # 更新元数据
    data['translation_pairs'] = new_pairs
    data['metadata']['total_pairs'] = len(new_pairs)
    data['metadata']['extraction_stats']['strategy_comments_pairs'] = strategy_pairs_count
    data['metadata']['extraction_stats']['total_pairs'] = len(new_pairs)
    
    # 保存更新后的文件
    with open('ml_translation_pairs.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 为新的翻译对创建单独文件
    individual_dir = Path('individual_pairs')
    
    # 重新创建所有单独文件
    for i, pair in enumerate(new_pairs, 1):
        # 清理文件名
        clean_filename = re.sub(r'[^\w\-_\.]', '_', pair['source_file'])
        if clean_filename.endswith('.txt'):
            clean_filename = clean_filename[:-4]
        
        if pair['section_type'] == 'STRATEGY_COMMENTS':
            filename = f"pair_{i:03d}_{clean_filename}_strategy.json"
        else:
            filename = f"pair_{i:03d}_{clean_filename}.json"
        
        file_path = individual_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({
                "id": i,
                "english": pair['english'],
                "chinese": pair['chinese'],
                "section_type": pair['section_type'],
                "source_file": pair['source_file'],
                "confidence": pair['confidence']
            }, f, ensure_ascii=False, indent=2)
    
    print(f"处理完成！")
    print(f"总翻译对数: {len(new_pairs)}")
    print(f"新增strategy comments翻译对: {strategy_pairs_count}")
    print(f"已为所有翻译对创建单独文件")

if __name__ == "__main__":
    process_translation_pairs()