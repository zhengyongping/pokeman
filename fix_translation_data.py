#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import re

def clean_chinese_text(text: str) -> str:
    """清理中文文本，移除配置信息"""
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        # 跳过Chinese Set配置行
        if (line.startswith('Chinese set:') or line.startswith('Chinese Set:') or 
            line.startswith('Chinese set：') or line.startswith('Chinese Set：')):
            continue
        # 跳过包含||分隔符的配置行
        if '||' in line and ('道具：' in line or '特性：' in line or '努力值：' in line or '性格：' in line or '招式：' in line):
            continue
        if line:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines).strip()

def fix_json_data():
    """修复JSON数据文件"""
    try:
        with open('ml_translation_pairs.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"原始翻译对数量: {len(data['translation_pairs'])}")
        
        # 清理每个翻译对的中文部分
        fixed_count = 0
        for pair in data['translation_pairs']:
            original_chinese = pair['chinese']
            cleaned_chinese = clean_chinese_text(original_chinese)
            
            if original_chinese != cleaned_chinese:
                pair['chinese'] = cleaned_chinese
                fixed_count += 1
                print(f"修复文件: {pair['source_file']}")
        
        print(f"\n修复的翻译对数量: {fixed_count}")
        
        # 保存修复后的数据
        with open('ml_translation_pairs_fixed.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("已保存修复后的JSON文件: ml_translation_pairs_fixed.json")
        
        return data
        
    except Exception as e:
        print(f"处理JSON文件时出错: {e}")
        return None

def fix_csv_data(data):
    """修复CSV数据文件"""
    if not data:
        return
    
    try:
        with open('ml_translation_pairs_fixed.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['english', 'chinese', 'section_type', 'source_file', 'confidence'])
            
            for pair in data['translation_pairs']:
                writer.writerow([
                    pair['english'],
                    pair['chinese'],
                    pair['section_type'],
                    pair['source_file'],
                    pair['confidence']
                ])
        
        print("已保存修复后的CSV文件: ml_translation_pairs_fixed.csv")
        
    except Exception as e:
        print(f"处理CSV文件时出错: {e}")

def main():
    print("开始修复翻译对数据...")
    print("="*50)
    
    # 修复JSON数据
    data = fix_json_data()
    
    # 修复CSV数据
    if data:
        fix_csv_data(data)
    
    print("\n修复完成！")
    print("修复后的文件:")
    print("- ml_translation_pairs_fixed.json")
    print("- ml_translation_pairs_fixed.csv")

if __name__ == "__main__":
    main()