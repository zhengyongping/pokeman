#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试爬虫程序
"""

from smogon_scraper import SmogonScraper
import os

def test_scraper():
    """测试爬虫功能"""
    print("开始测试爬虫程序...")
    
    # 创建爬虫实例
    scraper = SmogonScraper()
    
    # 测试URL
    test_url = "https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/"
    
    print(f"测试URL: {test_url}")
    
    try:
        # 运行爬虫
        scraper.scrape_chinese_archive(test_url)
        
        # 检查结果
        save_dir = "scraped_threads"
        if os.path.exists(save_dir):
            files = os.listdir(save_dir)
            print(f"\n成功保存了 {len(files)} 个文件")
            
            # 显示前几个文件
            for i, file in enumerate(files[:5]):
                file_path = os.path.join(save_dir, file)
                file_size = os.path.getsize(file_path)
                print(f"  {i+1}. {file} ({file_size} 字节)")
                
        else:
            print("\n没有创建保存目录")
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scraper()