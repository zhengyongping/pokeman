#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫保存功能演示程序
展示改进后的本地保存功能，包括多种格式和高级选项
"""

import os
import sys
from smogon_scraper import SmogonScraper

def demo_basic_save():
    """演示基础保存功能"""
    print("=== 基础保存功能演示 ===")
    
    # 创建爬虫实例
    scraper = SmogonScraper()
    
    # 添加一些示例数据
    scraper.translation_pairs = [
        {
            'english': 'Garchomp is a powerful Dragon/Ground-type Pokemon.',
            'chinese': '烈咬陆鲨是一只强大的龙/地面属性宝可梦。',
            'source': '演示数据',
            'type': 'demo_pair'
        },
        {
            'english': 'This Pokemon has excellent Attack and Speed stats.',
            'chinese': '这只宝可梦拥有出色的攻击和速度种族值。',
            'source': '演示数据',
            'type': 'demo_pair'
        },
        {
            'english': 'Earthquake is one of its signature moves.',
            'chinese': '地震是它的招牌技能之一。',
            'source': '演示数据',
            'type': 'demo_pair'
        }
    ]
    
    print(f"准备保存 {len(scraper.translation_pairs)} 个翻译对照")
    
    # 演示JSON格式保存
    print("\n1. 保存为JSON格式:")
    scraper.save_translations("demo_basic", "json")
    
    # 演示CSV格式保存
    print("\n2. 保存为CSV格式:")
    scraper.save_translations("demo_basic", "csv")
    
    # 演示TXT格式保存
    print("\n3. 保存为TXT格式:")
    scraper.save_translations("demo_basic", "txt")
    
    # 演示Excel格式保存（如果可用）
    print("\n4. 保存为Excel格式:")
    scraper.save_translations("demo_basic", "xlsx")

def demo_advanced_save():
    """演示高级保存功能"""
    print("\n=== 高级保存功能演示 ===")
    
    # 创建爬虫实例
    scraper = SmogonScraper()
    
    # 添加更多示例数据
    scraper.translation_pairs = [
        {
            'english': 'Competitive Pokemon battling requires strategic thinking.',
            'chinese': '竞技宝可梦对战需要战略思维。',
            'source': 'Smogon Strategy Guide',
            'type': 'strategy_guide'
        },
        {
            'english': 'Team building is crucial for success in tournaments.',
            'chinese': '组队对于在锦标赛中取得成功至关重要。',
            'source': 'Smogon Strategy Guide',
            'type': 'strategy_guide'
        },
        {
            'english': 'Understanding type matchups gives you an advantage.',
            'chinese': '理解属性相克关系能给你带来优势。',
            'source': 'Smogon Battle Guide',
            'type': 'battle_guide'
        },
        {
            'english': 'Speed control is essential in competitive play.',
            'chinese': '速度控制在竞技对战中至关重要。',
            'source': 'Smogon Battle Guide',
            'type': 'battle_guide'
        },
        {
            'english': 'Entry hazards can change the course of battle.',
            'chinese': '撒钉技能可以改变战斗的进程。',
            'source': 'Smogon Advanced Tactics',
            'type': 'advanced_tactics'
        }
    ]
    
    print(f"准备保存 {len(scraper.translation_pairs)} 个翻译对照")
    
    # 演示带统计信息的保存
    print("\n1. 保存带详细统计信息的JSON文件:")
    scraper.save_translations("demo_advanced", "json")
    
    # 演示自定义文件名和路径
    print("\n2. 保存到自定义路径:")
    custom_path = "custom_output/my_translations"
    scraper.save_translations(custom_path, "json")
    
    # 演示批量保存所有格式
    print("\n3. 批量保存所有格式:")
    for fmt in ['json', 'csv', 'txt']:
        try:
            scraper.save_translations(f"demo_all_formats", fmt)
        except Exception as e:
            print(f"保存{fmt}格式时出错: {e}")

def demo_file_management():
    """演示文件管理功能"""
    print("\n=== 文件管理演示 ===")
    
    # 检查保存的文件
    if os.path.exists("scraped_data"):
        print("\n已保存的文件:")
        for file in os.listdir("scraped_data"):
            file_path = os.path.join("scraped_data", file)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                print(f"  {file} ({file_size} 字节)")
    else:
        print("scraped_data 目录不存在")
    
    # 检查自定义路径的文件
    if os.path.exists("custom_output"):
        print("\n自定义路径的文件:")
        for file in os.listdir("custom_output"):
            file_path = os.path.join("custom_output", file)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                print(f"  {file} ({file_size} 字节)")

def demo_data_analysis():
    """演示数据分析功能"""
    print("\n=== 数据分析演示 ===")
    
    # 创建爬虫实例并添加数据
    scraper = SmogonScraper()
    scraper.translation_pairs = [
        {
            'english': 'Short text',
            'chinese': '短文本',
            'source': 'Source A',
            'type': 'type1'
        },
        {
            'english': 'This is a much longer piece of text that contains more words and characters.',
            'chinese': '这是一段更长的文本，包含更多的单词和字符。',
            'source': 'Source B',
            'type': 'type2'
        },
        {
            'english': 'Medium length text example',
            'chinese': '中等长度文本示例',
            'source': 'Source A',
            'type': 'type1'
        }
    ]
    
    # 获取统计信息
    stats = scraper._get_statistics()
    
    print("数据统计信息:")
    print(f"  总数量: {len(scraper.translation_pairs)}")
    
    if stats:
        print("\n长度统计:")
        length_stats = stats['length_statistics']
        print(f"  平均英文长度: {length_stats['avg_english_length']:.1f}")
        print(f"  平均中文长度: {length_stats['avg_chinese_length']:.1f}")
        print(f"  最长英文: {length_stats['max_english_length']}")
        print(f"  最长中文: {length_stats['max_chinese_length']}")
        
        print("\n来源分布:")
        for source, count in stats['source_distribution'].items():
            print(f"  {source}: {count}")
        
        print("\n类型分布:")
        for type_name, count in stats['type_distribution'].items():
            print(f"  {type_name}: {count}")

def main():
    """主演示函数"""
    print("Smogon爬虫保存功能演示程序")
    print("=" * 50)
    
    try:
        # 演示基础保存功能
        demo_basic_save()
        
        # 演示高级保存功能
        demo_advanced_save()
        
        # 演示文件管理
        demo_file_management()
        
        # 演示数据分析
        demo_data_analysis()
        
        print("\n=== 演示完成 ===")
        print("\n功能特点:")
        print("✓ 支持多种保存格式 (JSON, CSV, TXT, Excel)")
        print("✓ 自动创建保存目录")
        print("✓ 详细的统计信息")
        print("✓ 文件大小显示")
        print("✓ 数据分析功能")
        print("✓ 自定义保存路径")
        print("✓ 批量格式保存")
        
        print("\n使用建议:")
        print("• JSON格式适合程序读取")
        print("• CSV格式适合Excel分析")
        print("• TXT格式适合人工查看")
        print("• Excel格式提供最佳的数据分析体验")
        
    except Exception as e:
        print(f"演示过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()