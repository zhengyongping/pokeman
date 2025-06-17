#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from smogon_scraper import SmogonScraper

def test_first_post_scraping():
    """测试爬取主帖功能"""
    print("开始测试爬取主帖功能...")
    
    # 创建爬虫实例
    scraper = SmogonScraper()
    
    # 测试URL
    test_url = "https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/"
    
    try:
        # 爬取数据
        print(f"正在爬取: {test_url}")
        scraper.scrape_chinese_archive(test_url, max_threads=2)
        
        # 检查输出目录
        output_dir = "scraped_threads"
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            print(f"\n成功！共生成了 {len(files)} 个文件:")
            for file in files[:5]:  # 只显示前5个文件
                print(f"  - {file}")
            if len(files) > 5:
                print(f"  ... 还有 {len(files) - 5} 个文件")
        else:
            print("未找到输出目录")
            
    except Exception as e:
        print(f"测试失败: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = test_first_post_scraping()
    if success:
        print("\n✅ 测试完成")
    else:
        print("\n❌ 测试失败")
        sys.exit(1)