#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动筛选并删除scraped_threads目录中开头不是链接的文件
"""

import os
import re

def is_valid_url(text):
    """检查文本是否为有效的URL"""
    url_pattern = r'^https?://[^\s]+$'
    return bool(re.match(url_pattern, text.strip()))

def auto_filter_files():
    """自动筛选并删除无效文件"""
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
                    print(f"✓ 保留: {filename}")
                else:
                    invalid_files.append(filename)
                    print(f"✗ 标记删除: {filename} (开头: {first_line[:30]}...)")
                    
            except Exception as e:
                print(f"读取文件失败 {filename}: {e}")
                invalid_files.append(filename)
    
    print(f"\n=== 筛选结果 ===")
    print(f"有效文件数量: {len(valid_files)}")
    print(f"无效文件数量: {len(invalid_files)}")
    
    # 自动删除无效文件
    if invalid_files:
        print(f"\n开始删除无效文件...")
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
        print(f"保留 {len(valid_files)} 个有效文件")
    else:
        print("\n所有文件都是有效的！")

if __name__ == "__main__":
    auto_filter_files()