#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试交互式爬虫的核心功能
"""

import sys
import os

# 添加当前目录到路径
sys.path.append('.')

def test_single_url_scraping():
    """测试单个URL爬取功能"""
    try:
        from smogon_scraper import SmogonScraper
        
        # 测试URL
        test_url = "https://www.smogon.com/forums/threads/dd-xard.3737749/"
        
        print(f"测试爬取链接: {test_url}")
        
        scraper = SmogonScraper()
        save_dir = "scraped_threads"
        
        # 确保保存目录存在
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # 使用现有的_scrape_thread_to_file方法
        scraper._scrape_thread_to_file(test_url, save_dir)
        print("✓ 爬取完成")
        
        return True
        
    except Exception as e:
        print(f"✗ 爬取失败: {e}")
        return False

def test_url_validation():
    """测试URL验证功能"""
    from urllib.parse import urlparse
    
    def validate_smogon_url(url):
        try:
            parsed = urlparse(url)
            return (
                parsed.scheme in ['http', 'https'] and
                'smogon.com' in parsed.netloc and
                '/forums/threads/' in parsed.path
            )
        except:
            return False
    
    test_cases = [
        ("https://www.smogon.com/forums/threads/test.123456/", True),
        ("https://smogon.com/forums/threads/test.123456/", True),
        ("http://www.smogon.com/forums/threads/test.123456/", True),
        ("https://www.google.com", False),
        ("https://www.smogon.com/forums/", False),
        ("invalid-url", False)
    ]
    
    print("测试URL验证功能:")
    for url, expected in test_cases:
        result = validate_smogon_url(url)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {url} -> {result} (期望: {expected})")
    
    return True

def main():
    print("=" * 60)
    print("交互式爬虫功能测试")
    print("=" * 60)
    
    # 测试URL验证
    test_url_validation()
    
    print("\n" + "=" * 60)
    
    # 测试单个URL爬取
    test_single_url_scraping()
    
    print("\n测试完成")

if __name__ == "__main__":
    main()