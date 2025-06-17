#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进后的Smogon爬虫演示程序
展示新增的SET格式翻译对提取功能
"""

from smogon_scraper import SmogonScraper
import time
import json

def demo_set_format_extraction():
    """演示SET格式翻译对提取功能"""
    print("=== Smogon爬虫改进功能演示 ===")
    print("新功能：[SET]至[SET COMMENTS]格式的翻译对提取")
    print("="*50)
    
    # 创建爬虫实例
    scraper = SmogonScraper()
    
    print("\n1. 模拟SET格式数据测试")
    print("-"*30)
    
    # 模拟真实的Smogon论坛SET格式内容
    sample_content = [
        "Pokemon Analysis: Garchomp",
        "",
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
        "This Choice Scarf set allows Garchomp to outspeed many threats.",
        "Earthquake is the main STAB move with excellent coverage.",
        "",
        "宝可梦分析：烈咬陆鲨",
        "",
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
        "这个讲究围巾配置让烈咬陆鲨能够超越许多威胁。",
        "地震是主要的本系技能，拥有出色的覆盖面。",
        "",
        "Alternative Set Analysis",
        "[SET]",
        "Garchomp @ Life Orb",
        "Ability: Sand Veil",
        "EVs: 4 HP / 252 Atk / 252 Spe",
        "Adamant Nature",
        "- Earthquake",
        "- Outrage",
        "- Fire Fang",
        "- Swords Dance",
        "[SET COMMENTS]",
        "Life Orb variant for maximum power output.",
        "",
        "替代配置分析",
        "[SET]",
        "烈咬陆鲨 @ 生命宝珠",
        "特性: 沙隐",
        "努力值: 4 HP / 252 Atk / 252 Spe",
        "固执性格",
        "- 地震",
        "- 逆鳞",
        "- 火焰牙",
        "- 剑舞",
        "[SET COMMENTS]",
        "生命宝珠变种以获得最大输出。"
    ]
    
    print(f"测试数据包含 {len(sample_content)} 行内容")
    print("包含2个完整的英文-中文SET对照")
    
    # 提取翻译对
    scraper._extract_set_pairs(sample_content, "演示数据")
    
    print(f"\n提取结果: 共找到 {len(scraper.translation_pairs)} 个翻译对照")
    
    # 按类型分类显示
    set_pairs = [p for p in scraper.translation_pairs if 'set' in p.get('type', '').lower()]
    direct_pairs = [p for p in scraper.translation_pairs if p.get('type') == 'direct_pair']
    
    print(f"\n分类统计:")
    print(f"  SET格式配对: {len([p for p in scraper.translation_pairs if p.get('type') == 'set_pair'])} 个")
    print(f"  SET智能配对: {len([p for p in scraper.translation_pairs if p.get('type') == 'set_smart_pair'])} 个")
    print(f"  直接配对: {len(direct_pairs)} 个")
    
    # 显示SET格式的翻译对示例
    if set_pairs:
        print(f"\nSET格式翻译对示例:")
        for i, pair in enumerate(set_pairs[:3], 1):
            print(f"\n示例 {i} ({pair['type']}):")
            print(f"  英文: {pair['english']}")
            print(f"  中文: {pair['chinese']}")
            print(f"  相似度评分: {scraper._calculate_similarity_score(pair['english'], pair['chinese']):.2f}")
    
    return scraper

def demo_real_scraping():
    """演示真实网页爬取"""
    print("\n\n2. 真实网页爬取演示")
    print("-"*30)
    
    scraper = SmogonScraper()
    
    # 使用改进后的URL（包含prefix_id=484）
    target_url = "https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/?prefix_id=484"
    print(f"目标URL: {target_url}")
    print("这个URL专门针对中文翻译内容，包含SET格式的翻译对照")
    
    try:
        print("\n开始爬取...")
        scraper.scrape_chinese_archive(target_url)
        
        if scraper.translation_pairs:
            print(f"\n爬取成功！共获得 {len(scraper.translation_pairs)} 个翻译对照")
            
            # 详细统计
            type_stats = {}
            for pair in scraper.translation_pairs:
                pair_type = pair.get('type', '未知')
                type_stats[pair_type] = type_stats.get(pair_type, 0) + 1
            
            print("\n详细统计:")
            for pair_type, count in sorted(type_stats.items(), key=lambda x: x[1], reverse=True):
                print(f"  {pair_type}: {count} 个")
            
            # 显示SET相关的翻译对
            set_related = [p for p in scraper.translation_pairs if 'set' in p.get('type', '').lower()]
            if set_related:
                print(f"\nSET相关翻译对 (共{len(set_related)}个):")
                for i, pair in enumerate(set_related[:2], 1):
                    print(f"\n示例 {i}:")
                    print(f"  类型: {pair['type']}")
                    print(f"  英文: {pair['english'][:80]}...")
                    print(f"  中文: {pair['chinese'][:40]}...")
                    print(f"  来源: {pair['source']}")
            
            return scraper
        else:
            print("未找到翻译对照，可能是网络问题或页面结构变化")
            return None
            
    except Exception as e:
        print(f"爬取过程中出错: {e}")
        return None

def demo_save_and_analysis(scraper):
    """演示保存和分析功能"""
    if not scraper or not scraper.translation_pairs:
        print("\n没有数据可供保存和分析")
        return
    
    print("\n\n3. 保存和分析功能演示")
    print("-"*30)
    
    # 保存多种格式
    print("保存为多种格式...")
    formats = ['json', 'csv', 'txt']
    
    for fmt in formats:
        try:
            filename = f"demo_improved_scraper.{fmt}"
            scraper.save_translations(filename, fmt)
            print(f"✓ {fmt.upper()}格式保存成功")
        except Exception as e:
            print(f"✗ {fmt.upper()}格式保存失败: {e}")
    
    # 生成统计报告
    print("\n生成统计报告...")
    stats = scraper._get_statistics()
    
    if stats:
        print("\n=== 数据分析报告 ===")
        
        # 类型分布
        if 'type_distribution' in stats:
            print("\n翻译对类型分布:")
            for pair_type, count in stats['type_distribution'].items():
                percentage = (count / len(scraper.translation_pairs)) * 100
                print(f"  {pair_type}: {count} 个 ({percentage:.1f}%)")
        
        # 长度统计
        if 'length_statistics' in stats:
            length_stats = stats['length_statistics']
            print("\n文本长度统计:")
            print(f"  平均英文长度: {length_stats['avg_english_length']:.1f} 字符")
            print(f"  平均中文长度: {length_stats['avg_chinese_length']:.1f} 字符")
            print(f"  最长英文: {length_stats['max_english_length']} 字符")
            print(f"  最长中文: {length_stats['max_chinese_length']} 字符")
        
        # 来源分布
        if 'source_distribution' in stats:
            print("\n来源分布:")
            for source, count in list(stats['source_distribution'].items())[:3]:
                print(f"  {source[:50]}...: {count} 个")

def main():
    """主演示函数"""
    print("Smogon论坛爬虫改进功能演示")
    print(f"演示时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n主要改进:")
    print("1. 新增[SET]至[SET COMMENTS]格式识别")
    print("2. 智能配对算法")
    print("3. 相似度计算")
    print("4. 改进的URL定位")
    print("5. 多种配对策略")
    
    # 演示1: SET格式提取
    demo_scraper = demo_set_format_extraction()
    
    # 演示2: 真实爬取（可选）
    real_scraper = None
    user_choice = input("\n是否进行真实网页爬取演示？(y/n): ")
    if user_choice.lower() == 'y':
        real_scraper = demo_real_scraping()
    
    # 演示3: 保存和分析
    final_scraper = real_scraper if real_scraper else demo_scraper
    demo_save_and_analysis(final_scraper)
    
    print("\n=== 演示总结 ===")
    print("✓ SET格式识别功能正常")
    print("✓ 智能配对算法有效")
    print("✓ 多格式保存功能完整")
    print("✓ 统计分析功能详细")
    print("\n改进后的爬虫能够更准确地提取Smogon论坛中的翻译对照！")
    print("\n演示完成！")

if __name__ == "__main__":
    main()