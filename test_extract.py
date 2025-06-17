#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json

def test_single_file():
    """测试单个文件的提取"""
    file_path = "scraped_threads/National DexOgerpon-W.txt"
    
    print(f"测试文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"文件长度: {len(content)} 字符")
        
        # 查找分割线
        separator_full = "=" * 80 + "\nORIGINAL THREAD FIRST POST\n" + "=" * 80
        separator_simple = "=" * 80
        
        if separator_full in content:
            print("找到完整分割线")
            parts = content.split(separator_full)
        elif separator_simple in content:
            print("找到简单分割线")
            parts = content.split(separator_simple)
            print(f"分割后有 {len(parts)} 部分")
            # 过滤掉只包含"ORIGINAL THREAD FIRST POST"的部分
            filtered_parts = []
            for i, part in enumerate(parts):
                if "ORIGINAL THREAD FIRST POST" in part and len(part.strip()) < 50:
                    print(f"跳过部分 {i}: 只包含分割线标题")
                    continue
                filtered_parts.append(part)
            parts = filtered_parts
        else:
            print("没有找到分割线")
            return
        
        print(f"有效部分数量: {len(parts)}")
        
        if len(parts) >= 2:
            chinese_part = parts[0].strip()
            english_part = parts[1].strip()
            
            print(f"中文部分长度: {len(chinese_part)}")
            print(f"英文部分长度: {len(english_part)}")
            
            # 提取SET COMMENTS
            chinese_comments = extract_section(chinese_part, "[SET COMMENTS]")
            english_comments = extract_section(english_part, "[SET COMMENTS]")
            
            if chinese_comments and english_comments:
                print("\n=== 找到SET COMMENTS ===")
                print(f"中文长度: {len(chinese_comments)}")
                print(f"英文长度: {len(english_comments)}")
                
                # 清理中文部分
                chinese_clean = clean_chinese_comments(chinese_comments)
                print(f"清理后中文长度: {len(chinese_clean)}")
                
                # 保存结果
                result = {
                    'english': english_comments.strip(),
                    'chinese': chinese_clean.strip(),
                    'section': 'SET_COMMENTS',
                    'file': os.path.basename(file_path)
                }
                
                with open('test_result.json', 'w', encoding='utf-8') as f:
                    json.dump([result], f, ensure_ascii=False, indent=2)
                
                print("\n结果已保存到 test_result.json")
                print(f"\n英文预览: {english_comments[:200]}...")
                print(f"\n中文预览: {chinese_clean[:200]}...")
            else:
                print("没有找到SET COMMENTS部分")
                if not chinese_comments:
                    print("中文部分没有SET COMMENTS")
                if not english_comments:
                    print("英文部分没有SET COMMENTS")
        
    except Exception as e:
        print(f"处理文件时出错: {e}")

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

if __name__ == "__main__":
    test_single_file()