#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from smogon_scraper import SmogonScraper

def test_clean_output():
    """测试清洁输出功能（只保存纯文本内容）"""
    print("开始测试清洁输出功能...")
    
    # 创建爬虫实例
    scraper = SmogonScraper()
    
    # 测试URL
    test_url = "https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/"
    
    try:
        # 爬取数据
        print(f"正在爬取: {test_url}")
        scraper.scrape_chinese_archive(test_url, max_threads=1)
        
        # 检查输出目录
        output_dir = "scraped_threads"
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            print(f"\n成功！共生成了 {len(files)} 个文件")
            
            # 检查最新文件的内容格式
            if files:
                latest_file = max([os.path.join(output_dir, f) for f in files], key=os.path.getmtime)
                print(f"\n检查最新文件: {os.path.basename(latest_file)}")
                
                with open(latest_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                print(f"文件前5行内容:")
                for i, line in enumerate(lines[:5]):
                    print(f"  {i+1}: {line[:100]}{'...' if len(line) > 100 else ''}")
                    
                # 检查是否还包含爬取信息
                if "帖子标题:" in content or "来源链接:" in content or "爬取时间:" in content:
                    print("\n❌ 文件仍包含爬取信息头部")
                    return False
                else:
                    print("\n✅ 文件只包含纯文本内容")
                    return True
        else:
            print("未找到输出目录")
            return False
            
    except Exception as e:
        print(f"测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_clean_output()
    if success:
        print("\n✅ 测试完成 - 输出格式已优化")
    else:
        print("\n❌ 测试失败")
        sys.exit(1)