#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为每个翻译对创建单独的文件，保留[STRATEGY COMMENTS]等重要内容，只删除[CREDITS]等元数据
"""

import json
import os
import re
from pathlib import Path

def clean_chinese_text(text):
    """
    清理中文文本，只删除[CREDITS]相关的元数据信息，保留[STRATEGY COMMENTS]等重要内容
    """
    if not text:
        return text
    
    # 只删除[CREDITS]部分及其后的所有内容
    credits_pattern = r'\n\[CREDITS\][\s\S]*$'
    text = re.sub(credits_pattern, '', text)
    
    # 删除单独的Written by、Translated by、Grammar checked by等行
    metadata_patterns = [
        r'\nWritten by:[\s\S]*?(?=\n[^\s]|$)',
        r'\nTranslated by:[\s\S]*?(?=\n[^\s]|$)',
        r'\nGrammar checked by:[\s\S]*?(?=\n[^\s]|$)',
        r'\nQuality checked by:[\s\S]*?(?=\n[^\s]|$)',
    ]
    
    for pattern in metadata_patterns:
        text = re.sub(pattern, '', text)
    
    # 删除URL链接行
    text = re.sub(r'\nhttps://www\.smogon\.com/forums/members/[^\n]*', '', text)
    
    return text.strip()

def create_individual_files():
    """
    为每个翻译对创建单独的文件
    """
    # 读取原始文件
    input_file = '/Users/zhengyongping/test/AI-test/sctp/ml_translation_pairs.json'
    
    if not os.path.exists(input_file):
        print(f"错误：找不到文件 {input_file}")
        return
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 创建输出目录
    output_dir = Path('/Users/zhengyongping/test/AI-test/sctp/individual_pairs')
    output_dir.mkdir(exist_ok=True)
    
    # 清理现有文件
    for existing_file in output_dir.glob('*.json'):
        existing_file.unlink()
    
    translation_pairs = data.get('translation_pairs', [])
    cleaned_count = 0
    
    for i, pair in enumerate(translation_pairs):
        # 清理中文文本
        original_chinese = pair.get('chinese', '')
        cleaned_chinese = clean_chinese_text(original_chinese)
        
        if cleaned_chinese != original_chinese:
            cleaned_count += 1
        
        # 创建清理后的翻译对
        cleaned_pair = {
            'id': i + 1,
            'english': pair.get('english', ''),
            'chinese': cleaned_chinese,
            'section_type': pair.get('section_type', ''),
            'source_file': pair.get('source_file', ''),
            'confidence': pair.get('confidence', 1.0)
        }
        
        # 为每个翻译对创建单独文件
        filename = f"pair_{i+1:03d}_{pair.get('source_file', 'unknown').replace('.txt', '').replace(' ', '_')}.json"
        # 清理文件名中的特殊字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        output_file = output_dir / filename
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_pair, f, ensure_ascii=False, indent=2)
    
    # 更新原始文件
    updated_pairs = []
    for i, pair in enumerate(translation_pairs):
        cleaned_chinese = clean_chinese_text(pair.get('chinese', ''))
        updated_pair = pair.copy()
        updated_pair['chinese'] = cleaned_chinese
        updated_pairs.append(updated_pair)
    
    # 更新元数据
    updated_data = data.copy()
    updated_data['translation_pairs'] = updated_pairs
    updated_data['metadata']['cleaned_pairs'] = cleaned_count
    
    # 保存更新后的原始文件
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)
    
    print(f"处理完成！")
    print(f"- 总翻译对数量: {len(translation_pairs)}")
    print(f"- 清理的翻译对数量: {cleaned_count}")
    print(f"- 单独文件保存在: {output_dir}")
    print(f"- 原始文件已更新: {input_file}")
    
    # 显示清理示例
    if cleaned_count > 0:
        print("\n清理示例:")
        for i, pair in enumerate(translation_pairs[:3]):
            original = pair.get('chinese', '')
            cleaned = clean_chinese_text(original)
            if cleaned != original:
                print(f"\n翻译对 {i+1}:")
                print(f"原始长度: {len(original)} 字符")
                print(f"清理后长度: {len(cleaned)} 字符")
                if '[CREDITS]' in original:
                    print("- 删除了 [CREDITS] 部分")
                if 'Written by:' in original:
                    print("- 删除了作者信息")
                if 'https://www.smogon.com' in original:
                    print("- 删除了URL链接")
                break

if __name__ == '__main__':
    create_individual_files()