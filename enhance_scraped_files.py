#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强scraped_threads中的文件
读取每个文件第一行的链接，爬取thread的first post，并添加到文件中
"""

import os
import requests
from bs4 import BeautifulSoup
import time
import re

def get_first_post_content(url):
    """从给定URL获取thread的first post内容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 查找第一个帖子内容 - 尝试多种选择器
        selectors = [
            'div.message-body div.bbWrapper',
            'article.message-body div.bbWrapper', 
            'div.message-content div.bbWrapper',
            'div.bbWrapper',
            'div.message-body',
            'article.message-body',
            '.message-content'
        ]
        
        first_post = None
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                first_post = elements[0]  # 取第一个匹配的元素
                break
        
        if first_post:
            # 清理HTML标签，获取纯文本，保持分行格式
            text = first_post.get_text(separator='\n', strip=True)
            
            # 改进的文本清理逻辑，更好地保留分行格式
            # 1. 清理连续的空行，但保留段落间的分隔
            text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
            
            # 2. 按行处理，保持原有的行结构
            lines = text.split('\n')
            cleaned_lines = []
            
            for line in lines:
                # 只清理行内的多余空格，保持换行符
                if line.strip():  # 非空行
                    # 清理行内多个连续空格和制表符为单个空格
                    cleaned_line = re.sub(r'[ \t]+', ' ', line.strip())
                    cleaned_lines.append(cleaned_line)
                else:  # 空行
                    cleaned_lines.append('')  # 保留空行用于段落分隔
            
            # 3. 重新组合文本，保持分行结构
            text = '\n'.join(cleaned_lines)
            
            # 4. 最终清理：移除文件开头和结尾的多余空行
            text = text.strip()
            
            # 5. 确保段落间不超过两个换行符
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            return text
        else:
            # 如果找不到特定元素，尝试获取页面标题作为备用
            title = soup.find('title')
            if title:
                return f"无法解析帖子内容，页面标题: {title.get_text().strip()}"
            return "无法找到帖子内容"
            
    except Exception as e:
        return f"爬取失败: {str(e)}"

def enhance_scraped_files():
    """增强scraped_threads目录中的文件"""
    scraped_dir = '/Users/zhengyongping/test/AI-test/sctp/scraped_threads'
    
    if not os.path.exists(scraped_dir):
        print(f"目录不存在: {scraped_dir}")
        return
    
    processed_count = 0
    error_count = 0
    
    # 遍历目录中的所有txt文件
    for filename in sorted(os.listdir(scraped_dir)):
        if filename.endswith('.txt'):
            file_path = os.path.join(scraped_dir, filename)
            
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 获取第一行（链接）
                lines = content.split('\n')
                if not lines or not lines[0].strip():
                    print(f"跳过空文件: {filename}")
                    continue
                
                first_line = lines[0].strip()
                
                # 检查是否为有效链接
                if not first_line.startswith('http'):
                    print(f"跳过无效链接: {filename} - {first_line[:50]}...")
                    continue
                
                # 检查是否已经增强过（包含分割线）
                if '=' * 50 in content:
                    print(f"已处理过: {filename}")
                    continue
                
                print(f"处理文件: {filename}")
                print(f"链接: {first_line}")
                
                # 爬取first post内容
                first_post_content = get_first_post_content(first_line)
                
                if first_post_content and first_post_content != "无法找到帖子内容":
                    # 添加分割线和新内容
                    separator = '\n\n' + '=' * 80 + '\n'
                    separator += 'ORIGINAL THREAD FIRST POST\n'
                    separator += '=' * 80 + '\n\n'
                    
                    enhanced_content = content + separator + first_post_content
                    
                    # 写回文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(enhanced_content)
                    
                    print(f"✓ 成功增强: {filename}")
                    processed_count += 1
                else:
                    print(f"✗ 爬取失败: {filename} - {first_post_content}")
                    error_count += 1
                
                # 添加延迟避免被封
                time.sleep(2)
                
            except Exception as e:
                print(f"处理文件失败 {filename}: {e}")
                error_count += 1
    
    print(f"\n=== 处理完成 ===")
    print(f"成功处理: {processed_count} 个文件")
    print(f"处理失败: {error_count} 个文件")

if __name__ == "__main__":
    enhance_scraped_files()