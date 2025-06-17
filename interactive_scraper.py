#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式Smogon爬虫程序
允许用户输入链接进行爬取，并按照完整流程处理数据
流程：爬取 -> 筛选 -> 增强
"""

import os
import sys
import subprocess
import time
from urllib.parse import urlparse

def validate_smogon_url(url):
    """验证是否为有效的Smogon论坛链接"""
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ['http', 'https'] and
            'smogon.com' in parsed.netloc and
            '/forums/threads/' in parsed.path
        )
    except:
        return False

def run_script(script_name, description):
    """运行指定脚本并显示结果"""
    print(f"\n{'='*60}")
    print(f"正在执行: {description}")
    print(f"脚本: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            ['python3', script_name],
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        if result.returncode == 0:
            print(f"✓ {description} 完成")
            if result.stdout:
                print("输出:")
                print(result.stdout)
        else:
            print(f"✗ {description} 失败")
            if result.stderr:
                print("错误信息:")
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ {description} 超时")
        return False
    except Exception as e:
        print(f"✗ {description} 执行异常: {e}")
        return False
    
    return True

def get_user_input():
    """获取用户输入的链接"""
    print("\n" + "="*80)
    print("Smogon 交互式爬虫程序")
    print("="*80)
    print("\n请输入要爬取的Smogon论坛链接:")
    print("示例: https://www.smogon.com/forums/threads/thread-name.123456/")
    print("输入 'quit' 或 'exit' 退出程序")
    print("输入 'batch' 进入批量模式")
    
    while True:
        url = input("\n链接: ").strip()
        
        if url.lower() in ['quit', 'exit', 'q']:
            return None
        
        if url.lower() == 'batch':
            return 'batch'
        
        if not url:
            print("请输入有效的链接")
            continue
        
        if validate_smogon_url(url):
            return url
        else:
            print("无效的Smogon论坛链接，请重新输入")

def batch_mode():
    """批量模式：从文件读取链接"""
    print("\n" + "="*60)
    print("批量模式")
    print("="*60)
    
    # 创建示例文件
    sample_file = "urls.txt"
    if not os.path.exists(sample_file):
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write("# 在此文件中添加要爬取的链接，每行一个\n")
            f.write("# 以 # 开头的行为注释\n")
            f.write("# 示例:\n")
            f.write("# https://www.smogon.com/forums/threads/example.123456/\n")
        print(f"已创建示例文件: {sample_file}")
        print("请在文件中添加链接后重新运行批量模式")
        return []
    
    urls = []
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    if validate_smogon_url(line):
                        urls.append(line)
                    else:
                        print(f"警告: 第{line_num}行链接无效: {line}")
    except Exception as e:
        print(f"读取文件失败: {e}")
        return []
    
    print(f"从文件中读取到 {len(urls)} 个有效链接")
    return urls

def scrape_single_url(url):
    """爬取单个URL"""
    try:
        # 导入SmogonScraper类
        sys.path.append('.')
        from smogon_scraper import SmogonScraper
        
        print(f"开始爬取链接: {url}")
        
        scraper = SmogonScraper()
        save_dir = "scraped_threads"
        
        # 确保保存目录存在
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # 使用现有的_scrape_thread_to_file方法
        scraper._scrape_thread_to_file(url, save_dir)
        print("✓ 爬取完成")
        return True
        
    except Exception as e:
        print(f"✗ 爬取失败: {e}")
        return False

def cleanup_temp_files():
    """清理临时文件"""
    # 目前不需要清理临时文件
    pass

def main():
    """主函数"""
    try:
        while True:
            user_input = get_user_input()
            
            if user_input is None:
                print("\n程序退出")
                break
            
            urls_to_process = []
            
            if user_input == 'batch':
                urls_to_process = batch_mode()
                if not urls_to_process:
                    continue
            else:
                urls_to_process = [user_input]
            
            print(f"\n准备处理 {len(urls_to_process)} 个链接")
            
            for i, url in enumerate(urls_to_process, 1):
                print(f"\n{'='*80}")
                print(f"处理链接 {i}/{len(urls_to_process)}: {url}")
                print(f"{'='*80}")
                
                # 步骤1: 爬取数据
                if not scrape_single_url(url):
                    print(f"跳过链接 {i}: 爬取失败")
                    continue
                
                time.sleep(1)  # 短暂延迟
                
                # 步骤2: 筛选文件
                if not run_script('auto_filter_files.py', "文件筛选"):
                    print("警告: 文件筛选失败，继续下一步")
                
                time.sleep(1)
                
                # 步骤3: 增强文件
                if not run_script('enhance_scraped_files.py', "文件增强"):
                    print("警告: 文件增强失败")
                
                print(f"\n✓ 链接 {i} 处理完成")
                
                if i < len(urls_to_process):
                    time.sleep(2)  # 链接间延迟
            
            print(f"\n{'='*80}")
            print(f"所有链接处理完成！")
            print(f"处理的链接数量: {len(urls_to_process)}")
            print(f"结果保存在: scraped_threads/ 目录")
            print(f"{'='*80}")
            
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序异常: {e}")
    finally:
        cleanup_temp_files()

if __name__ == "__main__":
    main()