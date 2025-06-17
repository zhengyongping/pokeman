#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试SET格式配对功能
验证从同一帖子中提取英文和中文SET块并进行智能配对
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smogon_scraper import SmogonScraper
import json

def test_set_pairing():
    """测试SET配对功能"""
    print("=== 测试SET格式配对功能 ===")
    
    # 创建爬虫实例
    scraper = SmogonScraper()
    
    # 测试URL - 选择一个可能包含SET内容的帖子
    test_urls = [
        "https://www.smogon.com/forums/threads/特攻手猖狂，席多蓝恩来帮忙，火火又钢钢.3738979/",
        "https://www.smogon.com/forums/threads/剑舞领域大王-gp1-1.3763964/",
        "https://www.smogon.com/forums/threads/clefable.3738863/"
    ]
    
    for url in test_urls:
        print(f"\n测试URL: {url}")
        
        try:
            # 爬取单个帖子
            scraper.translation_pairs = []  # 清空之前的结果
            scraper._scrape_thread(url)
            
            if scraper.translation_pairs:
                print(f"找到 {len(scraper.translation_pairs)} 个翻译对")
                
                # 显示SET配对的结果
                set_pairs = [pair for pair in scraper.translation_pairs if pair['type'] == 'set_matched_pair']
                if set_pairs:
                    print(f"其中 {len(set_pairs)} 个是SET配对")
                    
                    for i, pair in enumerate(set_pairs[:3]):  # 显示前3个
                        print(f"\nSET配对 {i+1}:")
                        print(f"  匹配度: {pair.get('match_score', 'N/A')}")
                        print(f"  英文: {pair['english'][:100]}...")
                        print(f"  中文: {pair['chinese'][:100]}...")
                        print(f"  来源: {pair['source']}")
                else:
                    print("没有找到SET配对")
                    
                # 显示其他类型的翻译对
                other_pairs = [pair for pair in scraper.translation_pairs if pair['type'] != 'set_matched_pair']
                if other_pairs:
                    print(f"\n其他类型翻译对: {len(other_pairs)} 个")
                    type_counts = {}
                    for pair in other_pairs:
                        pair_type = pair['type']
                        type_counts[pair_type] = type_counts.get(pair_type, 0) + 1
                    
                    for pair_type, count in type_counts.items():
                        print(f"  {pair_type}: {count} 个")
            else:
                print("没有找到翻译对")
                
        except Exception as e:
            print(f"处理URL时出错: {e}")
            continue
            
        # 只测试第一个有结果的URL
        if scraper.translation_pairs:
            break
    
    # 保存测试结果
    if scraper.translation_pairs:
        output_file = "scraped_data/test_set_pairing.json"
        scraper.save_translations(output_file, 'json')
        print(f"\n测试结果已保存到: {output_file}")
        
        # 显示统计信息
        scraper.print_summary()
    else:
        print("\n测试完成，但没有找到任何翻译对")

def analyze_set_content():
    """分析SET内容的结构"""
    print("\n=== 分析SET内容结构 ===")
    
    # 模拟SET内容进行测试
    sample_lines = [
        "[SET]",
        "Pokemon: Garchomp",
        "Ability: Rough Skin",
        "Item: Life Orb",
        "Nature: Jolly",
        "EVs: 252 Atk / 4 HP / 252 Spe",
        "- Dragon Claw",
        "- Earthquake",
        "- Stone Edge",
        "- Swords Dance",
        "[SET COMMENTS]",
        "This is a standard physical Garchomp set.",
        "",
        "[SET]",
        "宝可梦: 烈咬陆鲨",
        "特性: 粗糙皮肤",
        "道具: 生命宝珠",
        "性格: 爽朗",
        "努力值: 252 攻击 / 4 HP / 252 速度",
        "- 龙爪",
        "- 地震",
        "- 尖石攻击",
        "- 剑舞",
        "[SET COMMENTS]",
        "这是一个标准的物理烈咬陆鲨配置。"
    ]
    
    scraper = SmogonScraper()
    
    # 测试SET提取
    scraper._extract_set_pairs(sample_lines, "测试来源")
    
    if scraper.translation_pairs:
        print(f"从样本中提取到 {len(scraper.translation_pairs)} 个翻译对")
        for pair in scraper.translation_pairs:
            print(f"\n类型: {pair['type']}")
            if 'match_score' in pair:
                print(f"匹配度: {pair['match_score']:.2f}")
            print(f"英文: {pair['english']}")
            print(f"中文: {pair['chinese']}")
    else:
        print("没有提取到翻译对")

def main():
    """主函数"""
    print("SET格式配对功能测试")
    print("=" * 50)
    
    # 确保输出目录存在
    os.makedirs("scraped_data", exist_ok=True)
    
    # 测试SET内容分析
    analyze_set_content()
    
    # 测试实际爬取
    test_set_pairing()
    
    print("\n测试完成！")

if __name__ == "__main__":
    main()