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
            
        # 跳过Chinese Set配置行（包含||分隔符的完整配置行）
        if (line.startswith('Chinese set:') or line.startswith('Chinese Set:') or
            line.startswith('Chinese set：') or line.startswith('Chinese Set：')):
            # 如果包含||分隔符，说明是完整的配置信息，跳过
            if '||' in line:
                continue
            # 如果不包含||，可能只是标题，也跳过
            continue
            
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def main():
    # 读取现有的翻译对数据
    with open('/Users/zhengyongping/test/AI-test/sctp/ml_translation_pairs.json', 'r', encoding='utf-8') as f:
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
    with open('/Users/zhengyongping/test/AI-test/sctp/ml_translation_pairs_cleaned.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 同时生成CSV格式
    import csv
    with open('/Users/zhengyongping/test/AI-test/sctp/ml_translation_pairs_cleaned.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['English', 'Chinese', 'Section_Type', 'Source_File', 'Confidence'])
        
        for pair in data['translation_pairs']:
            writer.writerow([
                pair['english'],
                pair['chinese'],
                pair['section_type'],
                pair['source_file'],
                pair['confidence']
            ])
    
    print(f"\n清理后的数据已保存到:")
    print(f"- ml_translation_pairs_cleaned.json")
    print(f"- ml_translation_pairs_cleaned.csv")

if __name__ == '__main__':
    main()