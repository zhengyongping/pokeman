#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json

def extract_translation_pairs(file_path):
    """从单个文件提取翻译对"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找分割线
        separator = "=" * 80 + "\nORIGINAL THREAD FIRST POST\n" + "=" * 80
        if separator in content:
            parts = content.split(separator)
        else:
            # 尝试简单分割线
            parts = content.split("=" * 80)
            if len(parts) >= 3:  # 有分割线标题的情况
                parts = [parts[0], parts[2]]  # 取第一部分和第三部分
        
        if len(parts) < 2:
            print(f"跳过 {os.path.basename(file_path)}: 没有找到分割线")
            return []
        
        chinese_part = parts[0].strip()
        english_part = parts[1].strip()
        
        pairs = []
        
        # 提取SET COMMENTS
        chinese_comments = extract_section(chinese_part, "[SET COMMENTS]")
        english_comments = extract_section(english_part, "[SET COMMENTS]")
        
        if chinese_comments and english_comments:
            # 清理中文部分的"Chinese Set:"行
            chinese_clean = clean_chinese_comments(chinese_comments)
            pairs.append({
                'english': english_comments.strip(),
                'chinese': chinese_clean.strip(),
                'section': 'SET_COMMENTS',
                'file': os.path.basename(file_path)
            })
        
        # 提取OVERVIEW
        chinese_overview = extract_section(chinese_part, "[OVERVIEW]")
        english_overview = extract_section(english_part, "[OVERVIEW]")
        
        if chinese_overview and english_overview:
            pairs.append({
                'english': english_overview.strip(),
                'chinese': chinese_overview.strip(),
                'section': 'OVERVIEW',
                'file': os.path.basename(file_path)
            })
        
        # 提取STRATEGY COMMENTS
        chinese_strategy = extract_section(chinese_part, "[STRATEGY COMMENTS]")
        english_strategy = extract_section(english_part, "[STRATEGY COMMENTS]")
        
        if chinese_strategy and english_strategy:
            pairs.append({
                'english': english_strategy.strip(),
                'chinese': chinese_strategy.strip(),
                'section': 'STRATEGY_COMMENTS',
                'file': os.path.basename(file_path)
            })
        
        return pairs
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return []

def extract_section(text, section_name):
    """提取指定章节的内容"""
    pattern = rf'{re.escape(section_name)}\s*\n(.*?)(?=\n\[|$)'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else None

def clean_chinese_comments(text):
    """清理中文注释中的Chinese Set行"""
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if not line.strip().startswith('Chinese Set:'):
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def main():
    scraped_dir = "scraped_threads"
    
    if not os.path.exists(scraped_dir):
        print(f"目录 {scraped_dir} 不存在")
        return
    
    all_pairs = []
    files = [f for f in os.listdir(scraped_dir) if f.endswith('.txt')]
    
    print(f"找到 {len(files)} 个文件")
    
    for i, filename in enumerate(files[:3]):  # 只处理前3个文件进行测试
        file_path = os.path.join(scraped_dir, filename)
        print(f"处理文件 {i+1}/{min(3, len(files))}: {filename}")
        
        pairs = extract_translation_pairs(file_path)
        all_pairs.extend(pairs)
        
        print(f"  提取到 {len(pairs)} 个翻译对")
    
    print(f"\n总计提取到 {len(all_pairs)} 个翻译对")
    
    # 保存结果
    if all_pairs:
        with open('translation_pairs_sample.json', 'w', encoding='utf-8') as f:
            json.dump(all_pairs, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到 translation_pairs_sample.json")
        
        # 显示示例
        print("\n=== 示例翻译对 ===")
        for i, pair in enumerate(all_pairs[:2]):
            print(f"\n翻译对 {i+1} ({pair['section']})：")
            print(f"英文: {pair['english'][:100]}...")
            print(f"中文: {pair['chinese'][:100]}...")

if __name__ == "__main__":
    main()