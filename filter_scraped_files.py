#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
筛选scraped_threads目录中的文件
保留开头为链接的有效文本，删除开头不是链接的无效文本
"""

import os
import re

def is_valid_url(text):
    """检查文本是否为有效的URL"""
    url_pattern = r'^https?://[^\s]+$'
    return bool(re.match(url_pattern, text.strip()))

def filter_scraped_files():
    """筛选scraped_threads目录中的文件"""
    scraped_dir = '/Users/zhengyongping/test/AI-test/sctp/scraped_threads'
    
    if not os.path.exists(scraped_dir):
        print(f"目录不存在: {scraped_dir}")
        return
    
    valid_files = []
    invalid_files = []
    
    # 遍历目录中的所有文件
    for filename in os.listdir(scraped_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(scraped_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                
                # 检查第一行是否为链接
                if is_valid_url(first_line):
                    valid_files.append(filename)
                    print(f"✓ 有效文件: {filename} (开头: {first_line[:50]}...)")
                else:
                    invalid_files.append(filename)
                    print(f"✗ 无效文件: {filename} (开头: {first_line[:50]}...)")
                    
            except Exception as e:
                print(f"读取文件失败 {filename}: {e}")
                invalid_files.append(filename)
    
    print(f"\n=== 筛选结果 ===")
    print(f"有效文件数量: {len(valid_files)}")
    print(f"无效文件数量: {len(invalid_files)}")
    
    if invalid_files:
        print(f"\n无效文件列表:")
        for filename in invalid_files:
            print(f"  - {filename}")
        
        # 询问是否删除无效文件
        response = input(f"\n是否删除这 {len(invalid_files)} 个无效文件? (y/N): ")
        if response.lower() in ['y', 'yes', '是']:
            deleted_count = 0
            for filename in invalid_files:
                file_path = os.path.join(scraped_dir, filename)
                try:
                    os.remove(file_path)
                    print(f"已删除: {filename}")
                    deleted_count += 1
                except Exception as e:
                    print(f"删除失败 {filename}: {e}")
            
            print(f"\n成功删除 {deleted_count} 个无效文件")
        else:
            print("取消删除操作")
    else:
        print("\n所有文件都是有效的！")

if __name__ == "__main__":
    filter_scraped_files()