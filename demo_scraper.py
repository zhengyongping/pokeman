#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smogon爬虫演示程序
展示如何使用新的爬虫功能从Smogon论坛学习翻译内容
"""

import sys
import os
from translator import PersonalizedTranslator

def demo_scraper():
    """演示爬虫功能"""
    print("=== Smogon论坛翻译内容爬虫演示 ===")
    print()
    
    # 创建翻译器实例
    translator = PersonalizedTranslator()
    
    print("当前翻译器状态:")
    print(f"- 已有翻译样本: {len(translator.translation_pairs)} 个")
    print()
    
    # 询问用户是否要运行爬虫
    print("此程序将从以下网址爬取翻译内容:")
    print("https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/")
    print()
    print("注意事项:")
    print("1. 爬虫会访问Smogon论坛，请确保网络连接正常")
    print("2. 爬虫会自动添加延迟，避免对服务器造成压力")
    print("3. 首次运行可能需要几分钟时间")
    print("4. 爬取的内容将自动保存到translation_data.json")
    print()
    
    choice = input("是否开始爬取？(y/n): ")
    if choice.lower() != 'y':
        print("已取消爬取")
        return
        
    print("\n开始爬取Smogon翻译内容...")
    print("=" * 50)
    
    try:
        # 记录初始样本数量
        initial_count = len(translator.translation_pairs)
        
        # 开始学习
        translator.learn_from_smogon()
        
        # 计算新增样本数量
        new_count = len(translator.translation_pairs) - initial_count
        
        print("=" * 50)
        print("\n爬取完成！")
        print(f"新增翻译样本: {new_count} 个")
        print(f"总翻译样本: {len(translator.translation_pairs)} 个")
        
        # 保存数据
        translator.save_data()
        print("翻译数据已保存")
        
        # 显示一些示例
        if new_count > 0:
            print("\n新学习的翻译示例:")
            recent_samples = translator.translation_pairs[-min(3, new_count):]
            for i, sample in enumerate(recent_samples, 1):
                print(f"\n示例 {i}:")
                print(f"英文: {sample['english'][:80]}..." if len(sample['english']) > 80 else f"英文: {sample['english']}")
                print(f"中文: {sample['chinese'][:60]}..." if len(sample['chinese']) > 60 else f"中文: {sample['chinese']}")
        
        # 测试翻译效果
        print("\n=== 翻译效果测试 ===")
        test_sentences = [
            "This Pokemon is a powerful physical sweeper",
            "Scizor can check most special attackers",
            "The current metagame favors defensive walls"
        ]
        
        for sentence in test_sentences:
            translation = translator.personalized_translate(sentence)
            print(f"\n原文: {sentence}")
            print(f"译文: {translation}")
            
    except KeyboardInterrupt:
        print("\n用户中断了爬取过程")
    except Exception as e:
        print(f"\n爬取过程中出现错误: {e}")
        print("请检查网络连接或稍后重试")
        
def demo_manual_scraper():
    """演示手动使用爬虫"""
    print("=== 手动爬虫演示 ===")
    print()
    
    try:
        from smogon_scraper import SmogonScraper
        
        # 创建爬虫实例
        scraper = SmogonScraper()
        
        print("开始爬取Smogon中文翻译存档...")
        
        # 爬取内容
        scraper.scrape_chinese_archive()
        
        # 显示结果摘要
        scraper.print_summary()
        
        # 保存结果
        scraper.save_translations("manual_scraper_results.json")
        
        print("\n手动爬虫演示完成！")
        
    except ImportError:
        print("无法导入smogon_scraper模块")
    except Exception as e:
        print(f"手动爬虫演示出错: {e}")
        
def main():
    """主函数"""
    print("Smogon翻译内容爬虫演示程序")
    print("=" * 40)
    print()
    print("请选择演示模式:")
    print("1. 集成爬虫演示（推荐）- 直接集成到翻译器")
    print("2. 手动爬虫演示 - 独立运行爬虫")
    print("3. 退出")
    print()
    
    while True:
        choice = input("请输入选择 (1-3): ")
        
        if choice == '1':
            demo_scraper()
            break
        elif choice == '2':
            demo_manual_scraper()
            break
        elif choice == '3':
            print("再见！")
            break
        else:
            print("无效选择，请输入 1-3")
            
if __name__ == "__main__":
    main()