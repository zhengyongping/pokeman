#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re

def clean_chinese_text(text):
    """只删除[CREDITS]相关内容，保留[STRATEGY COMMENTS]"""
    if not text:
        return text
    
    # 删除[CREDITS]部分
    text = re.sub(r'\[CREDITS\][\s\S]*$', '', text, flags=re.IGNORECASE)
    
    # 删除作者信息行
    patterns = [
        r'Written by:.*?\n?',
        r'Quality checked by:.*?\n?', 
        r'Translated by:.*?\n?',
        r'Grammar checked by:.*?\n?'
    ]
    
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    return text.strip()

def main():
    # 读取数据
    with open('/Users/zhengyongping/test/AI-test/sctp/ml_translation_pairs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 创建输出目录
    output_dir = '/Users/zhengyongping/test/AI-test/sctp/individual_pairs'
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理每个翻译对
    for i, pair in enumerate(data['translation_pairs']):
        # 清理中文文本
        cleaned_chinese = clean_chinese_text(pair['chinese'])
        
        # 创建清理后的翻译对
        cleaned_pair = {
            'id': i + 1,
            'english': pair['english'],
            'chinese': cleaned_chinese,
            'section_type': pair['section_type'],
            'source_file': pair['source_file'],
            'confidence': pair['confidence']
        }
        
        # 创建文件名
        safe_filename = re.sub(r'[^\w\-_\.]', '_', pair['source_file'])
        filename = f'pair_{i+1:03d}_{safe_filename}.json'
        filepath = os.path.join(output_dir, filename)
        
        # 保存单独文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(cleaned_pair, f, ensure_ascii=False, indent=2)
        
        print(f'创建文件: {filename}')
        
        # 更新原数据
        data['translation_pairs'][i]['chinese'] = cleaned_chinese
    
    # 保存更新后的原文件
    with open('/Users/zhengyongping/test/AI-test/sctp/ml_translation_pairs.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f'\n完成！处理了 {len(data["translation_pairs"])} 个翻译对')
    print(f'单独文件保存在: {output_dir}')

if __name__ == '__main__':
    main()