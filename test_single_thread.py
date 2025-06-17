#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def test_single_thread_clean_output():
    """测试单个帖子的清洁输出"""
    print("开始测试单个帖子的清洁输出...")
    
    # 测试URL - 直接使用一个帖子链接
    thread_url = "https://www.smogon.com/forums/threads/scarf-kyo-gp1-1.3764257/"
    
    try:
        # 创建session
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        print(f"正在访问: {thread_url}")
        response = session.get(thread_url, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 获取帖子标题
        title_elem = soup.find('h1', class_='p-title-value')
        title = title_elem.get_text(strip=True) if title_elem else "测试帖子"
        print(f"帖子标题: {title}")
        
        # 清理标题作为文件名
        safe_title = title.replace('/', '_').replace('\\', '_').replace(':', '_')
        safe_title = safe_title.replace('<', '_').replace('>', '_').replace('|', '_')
        safe_title = safe_title.replace('?', '_').replace('*', '_').replace('"', '_')
        
        # 查找帖子内容
        posts = soup.find_all('div', class_='bbWrapper')
        
        if posts:
            first_post = posts[0]  # 主帖
            text_content = first_post.get_text(separator='\n', strip=True)
            
            # 保存到新文件（测试清洁输出）
            output_dir = "scraped_threads"
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"TEST_CLEAN_{safe_title}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # 只保存纯文本内容
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text_content)
                
            print(f"\n✅ 已保存清洁版本到: {filepath}")
            print(f"文件大小: {len(text_content)} 字符")
            
            # 显示前几行内容
            lines = text_content.split('\n')
            print(f"\n文件前5行内容:")
            for i, line in enumerate(lines[:5]):
                if line.strip():
                    print(f"  {i+1}: {line[:80]}{'...' if len(line) > 80 else ''}")
                    
            return True
        else:
            print("未找到帖子内容")
            return False
            
    except Exception as e:
        print(f"测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_single_thread_clean_output()
    if success:
        print("\n✅ 单帖测试完成 - 清洁输出格式正常")
    else:
        print("\n❌ 单帖测试失败")