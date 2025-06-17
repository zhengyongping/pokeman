#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试网络连接和HTML解析
"""

import requests
from bs4 import BeautifulSoup
import os
import time

def test_basic_connection():
    """测试基本网络连接"""
    print("测试网络连接...")
    
    url = "https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/"
    
    try:
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        print(f"正在访问: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"状态码: {response.status_code}")
        print(f"响应长度: {len(response.content)} 字节")
        
        if response.status_code == 200:
            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找帖子链接
            thread_links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and '/threads/' in href:
                    if href.startswith('/'):
                        href = 'https://www.smogon.com' + href
                    thread_links.append(href)
                    
            print(f"找到 {len(thread_links)} 个帖子链接")
            
            # 显示前几个链接
            for i, link in enumerate(thread_links[:3]):
                print(f"  {i+1}. {link}")
                
            # 测试访问第一个帖子
            if thread_links:
                test_thread_url = thread_links[0]
                print(f"\n测试访问第一个帖子: {test_thread_url}")
                
                thread_response = requests.get(test_thread_url, headers=headers, timeout=15)
                print(f"帖子状态码: {thread_response.status_code}")
                
                if thread_response.status_code == 200:
                    thread_soup = BeautifulSoup(thread_response.content, 'html.parser')
                    
                    # 获取标题
                    title_elem = thread_soup.find('h1', class_='p-title-value')
                    title = title_elem.get_text(strip=True) if title_elem else "未知标题"
                    print(f"帖子标题: {title}")
                    
                    # 查找回复内容
                    posts = thread_soup.find_all('div', class_='bbWrapper')
                    print(f"找到 {len(posts)} 个帖子内容块")
                    
                    if len(posts) > 1:
                        first_reply = posts[1]
                        reply_text = first_reply.get_text(separator='\n', strip=True)
                        print(f"第一个回复长度: {len(reply_text)} 字符")
                        print(f"第一个回复前100字符: {reply_text[:100]}...")
                        
                        # 测试保存文件
                        save_dir = "test_output"
                        if not os.path.exists(save_dir):
                            os.makedirs(save_dir)
                            
                        # 清理文件名
                        safe_title = title.replace('/', '_').replace('\\', '_').replace(':', '_')
                        safe_title = safe_title.replace('<', '_').replace('>', '_').replace('|', '_')
                        safe_title = safe_title.replace('?', '_').replace('*', '_').replace('"', '_')
                        
                        filename = f"{safe_title}.txt"
                        filepath = os.path.join(save_dir, filename)
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(f"帖子标题: {title}\n")
                            f.write(f"来源链接: {test_thread_url}\n")
                            f.write(f"爬取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write("=" * 50 + "\n\n")
                            f.write(reply_text)
                            
                        print(f"\n测试文件已保存: {filepath}")
                        print(f"文件大小: {os.path.getsize(filepath)} 字节")
                        
                    else:
                        print("没有找到回复内容")
                        
        else:
            print(f"访问失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_basic_connection()