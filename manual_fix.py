#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

def clean_chinese_text(text):
    """清理中文翻译文本，移除Chinese Set配置信息"""
    if not text:
        return text
    
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 跳过所有包含Chinese set/Set的行
        if ('Chinese set' in line or 'Chinese Set' in line):
            continue
            
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

# 读取现有的翻译对数据
with open('ml_translation_pairs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"原始数据包含 {len(data['translation_pairs'])} 对翻译")

# 清理翻译对
cleaned_count = 0
for pair in data['translation_pairs']:
    original_chinese = pair['chinese']
    cleaned_chinese = clean_chinese_text(original_chinese)
    
    if cleaned_chinese != original_chinese:
        pair['chinese'] = cleaned_chinese
        cleaned_count += 1
        print(f"清理了文件 {pair['source_file']} 中的翻译对")

print(f"\n总共清理了 {cleaned_count} 对翻译")

# 保存清理后的数据
with open('ml_translation_pairs_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n清理后的数据已保存到 ml_translation_pairs_cleaned.json")
print("程序执行完成")