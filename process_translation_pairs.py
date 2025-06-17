#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re

def clean_chinese_text(text):
    """
    清理中文文本，只删除[CREDITS]相关内容，保留[STRATEGY COMMENTS]等重要信息
    """
    if not text:
        return text
    
    # 只删除[CREDITS]部分及其相关的元数据
    credits_pattern = r'\[CREDITS\][\s\S]*?(?=\[|$)'
    text = re.sub(credits_pattern, '', text, flags=re.IGNORECASE)
    
    # 删除单独的作者信息行
    author_patterns = [
        r'Written by:.*?\n',
        r'Quality checked by:.*?\n', 
        r'Translated by:.*?\n',
        r'Grammar checked by:.*?\n'
    ]
    
    for pattern in author_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # 清理多余的空行
    text = re.sub(r'\n\s*\n', '\n', text)
    text = text.strip()
    
    return text

def process_translation_pairs():
    """
    处理翻译对数据：清理数据并创建单独文件
    """
    input_file = '/Users/zhengyongping/test/AI-test/sctp/ml_translation_pairs.json'
    output_dir = '/Users/zhengyongping/test/AI-test/sctp/individual_pairs'
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取原始数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_pairs = []
    
    for i, pair in enumerate(data['translation_pairs']):
        # 清理中文文本
        original_chinese = pair['chinese']
        cleaned_chinese = clean_chinese_text(original_chinese)
        
        # 创建清理后的翻译对
        cleaned_pair = {
            'english': pair['english'],
            'chinese': cleaned_chinese,
            'section_type': pair['section_type'],
            'source_file': pair['source_file'],
            'confidence': pair['confidence']
        }
        
        cleaned_pairs.append(cleaned_pair)
        
        # 为每个翻译对创建单独文件
        pair_filename = f'pair_{i+1:03d}_{pair["source_file"].replace(".txt", "").replace(" ", "_")}.json'
        pair_filepath = os.path.join(output_dir, pair_filename)
        
        with open(pair_filepath, 'w', encoding='utf-8') as f:
            json.dump(cleaned_pair, f, ensure_ascii=False, indent=2)
        
        print(f"创建文件: {pair_filename}")
    
    # 更新原始文件
    data['translation_pairs'] = cleaned_pairs
    data['metadata']['cleaned_pairs'] = len(cleaned_pairs)
    
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n处理完成！")
    print(f"- 总共处理了 {len(cleaned_pairs)} 个翻译对")
    print(f"- 单独文件保存在: {output_dir}")
    print(f"- 原始文件已更新")

if __name__ == '__main__':
    process_translation_pairs()