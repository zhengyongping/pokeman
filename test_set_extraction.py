#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试SET格式翻译对提取功能
"""

from smogon_scraper import SmogonScraper
import time

def test_set_extraction():
    """测试SET格式的翻译对提取"""
    print("=== 测试SET格式翻译对提取功能 ===")
    
    # 创建爬虫实例
    scraper = SmogonScraper()
    
    # 模拟包含SET格式的文本内容
    test_lines = [
        "Pokemon Analysis",
        "[SET]",
        "Garchomp @ Choice Scarf",
        "Ability: Rough Skin",
        "EVs: 4 HP / 252 Atk / 252 Spe",
        "Jolly Nature",
        "- Earthquake",
        "- Dragon Claw",
        "- Stone Edge",
        "- U-turn",
        "[SET COMMENTS]",
        "This set focuses on speed and power.",
        "",
        "宝可梦分析",
        "[SET]",
        "烈咬陆鲨 @ 讲究围巾",
        "特性: 粗糙皮肤",
        "努力值: 4 HP / 252 Atk / 252 Spe",
        "爽朗性格",
        "- 地震",
        "- 龙爪",
        "- 尖石攻击",
        "- 急速折返",
        "[SET COMMENTS]",
        "这个配置专注于速度和力量。",
        "",
        "Another analysis section",
        "[SET]",
        "Dragonite @ Leftovers",
        "Ability: Multiscale",
        "EVs: 252 HP / 4 Atk / 252 SpA",
        "Modest Nature",
        "- Hurricane",
        "- Fire Blast",
        "- Roost",
        "- Thunder Wave",
        "[SET COMMENTS]",
        "Mixed attacker with good bulk.",
        "",
        "另一个分析部分",
        "[SET]",
        "快龙 @ 剩饭",
        "特性: 多重鳞片",
        "努力值: 252 HP / 4 Atk / 252 SpA",
        "内敛性格",
        "- 暴风",
        "- 大字爆炎",
        "- 羽栖",
        "- 电磁波",
        "[SET COMMENTS]",
        "具有良好耐久的混合攻击手。"
    ]
    
    print(f"测试数据包含 {len(test_lines)} 行")
    print("\n开始提取SET格式翻译对...")
    
    # 测试SET格式提取
    scraper._extract_set_pairs(test_lines, "测试来源")
    
    print(f"\n提取结果:")
    print(f"共找到 {len(scraper.translation_pairs)} 个翻译对照")
    
    # 显示提取的翻译对
    for i, pair in enumerate(scraper.translation_pairs, 1):
        print(f"\n翻译对 {i}:")
        print(f"  英文: {pair['english']}")
        print(f"  中文: {pair['chinese']}")
        print(f"  类型: {pair['type']}")
        print(f"  来源: {pair['source']}")
    
    # 保存测试结果
    if scraper.translation_pairs:
        print("\n保存测试结果...")
        scraper.save_translations("test_set_extraction", "json")
        scraper.save_translations("test_set_extraction", "csv")
        print("测试结果已保存")
    
    return len(scraper.translation_pairs)

def test_real_scraping():
    """测试真实的网页爬取"""
    print("\n=== 测试真实网页爬取 ===")
    
    scraper = SmogonScraper()
    
    # 爬取指定URL
    target_url = "https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/?prefix_id=484"
    print(f"开始爬取: {target_url}")
    
    try:
        scraper.scrape_chinese_archive(target_url)
        
        print(f"\n爬取完成！")
        print(f"共获得 {len(scraper.translation_pairs)} 个翻译对照")
        
        # 按类型统计
        type_count = {}
        for pair in scraper.translation_pairs:
            pair_type = pair.get('type', '未知')
            type_count[pair_type] = type_count.get(pair_type, 0) + 1
        
        print("\n按类型统计:")
        for pair_type, count in type_count.items():
            print(f"  {pair_type}: {count} 个")
        
        # 显示一些SET类型的示例
        set_pairs = [p for p in scraper.translation_pairs if 'set' in p.get('type', '').lower()]
        if set_pairs:
            print(f"\nSET类型翻译对示例 (共{len(set_pairs)}个):")
            for i, pair in enumerate(set_pairs[:3], 1):
                print(f"\n示例 {i}:")
                print(f"  英文: {pair['english'][:100]}...")
                print(f"  中文: {pair['chinese'][:50]}...")
                print(f"  类型: {pair['type']}")
        
        # 保存结果
        if scraper.translation_pairs:
            print("\n保存爬取结果...")
            scraper.save_translations("real_scraping_with_set", "json")
            scraper.save_translations("real_scraping_with_set", "csv")
            
        return len(scraper.translation_pairs)
        
    except Exception as e:
        print(f"爬取过程中出错: {e}")
        return 0

def main():
    """主测试函数"""
    print("开始测试改进后的Smogon爬虫...")
    print(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试1: SET格式提取
    mock_count = test_set_extraction()
    
    # 测试2: 真实爬取（可选）
    real_count = 0
    user_choice = input("\n是否进行真实网页爬取测试？(y/n): ")
    if user_choice.lower() == 'y':
        real_count = test_real_scraping()
    
    # 总结
    print("\n=== 测试总结 ===")
    print(f"模拟测试提取翻译对: {mock_count} 个")
    print(f"真实爬取翻译对: {real_count} 个")
    print("\n改进功能:")
    print("✓ 新增[SET]至[SET COMMENTS]格式识别")
    print("✓ 智能配对算法")
    print("✓ 相似度计算")
    print("✓ 多种配对策略")
    print("\n测试完成！")

if __name__ == "__main__":
    main()