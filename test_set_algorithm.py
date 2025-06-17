#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试SET配对算法
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smogon_scraper import SmogonScraper
import json

def test_set_extraction_algorithm():
    """测试SET提取算法"""
    print("=== 测试SET提取算法 ===")
    
    # 创建测试数据 - 模拟一个包含英文和中文SET的帖子内容
    test_content = [
        "这是一个测试帖子",
        "",
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
        "This is a standard physical Garchomp set that can sweep teams.",
        "It has great coverage and power.",
        "",
        "一些其他内容",
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
        "这是一个标准的物理烈咬陆鲨配置，可以横扫队伍。",
        "它有很好的覆盖面和威力。",
        "",
        "更多内容",
        "",
        "[SET]",
        "Pokemon: Dragapult",
        "Ability: Clear Body",
        "Item: Choice Band", 
        "Nature: Jolly",
        "EVs: 252 Atk / 4 HP / 252 Spe",
        "- Dragon Darts",
        "- Phantom Force",
        "- U-turn",
        "- Steel Wing",
        "[SET COMMENTS]",
        "Choice Band Dragapult is a powerful physical attacker.",
        "",
        "[SET]",
        "宝可梦: 多龙巴鲁托",
        "特性: 恒净之躯",
        "道具: 讲究头带",
        "性格: 爽朗", 
        "努力值: 252 攻击 / 4 HP / 252 速度",
        "- 龙箭",
        "- 潜灵奇袭",
        "- 急速折返",
        "- 钢翼",
        "[SET COMMENTS]",
        "讲究头带多龙巴鲁托是一个强力的物理攻击手。"
    ]
    
    # 创建爬虫实例并测试
    scraper = SmogonScraper()
    
    print(f"测试内容包含 {len(test_content)} 行")
    
    # 调用SET提取方法
    scraper._extract_set_pairs(test_content, "测试来源")
    
    print(f"\n提取结果: {len(scraper.translation_pairs)} 个翻译对")
    
    if scraper.translation_pairs:
        for i, pair in enumerate(scraper.translation_pairs):
            print(f"\n翻译对 {i+1}:")
            print(f"  类型: {pair['type']}")
            if 'match_score' in pair:
                print(f"  匹配度: {pair['match_score']:.3f}")
            print(f"  英文 ({len(pair['english'])} 字符): {pair['english'][:100]}...")
            print(f"  中文 ({len(pair['chinese'])} 字符): {pair['chinese'][:100]}...")
            print(f"  来源: {pair['source']}")
    else:
        print("没有提取到翻译对")
        
    return scraper.translation_pairs

def test_set_block_extraction():
    """测试SET块提取"""
    print("\n=== 测试SET块提取 ===")
    
    test_lines = [
        "[SET]",
        "Pokemon: Garchomp", 
        "Ability: Rough Skin",
        "[SET COMMENTS]",
        "This is a comment",
        "",
        "[SET]",
        "宝可梦: 烈咬陆鲨",
        "特性: 粗糙皮肤",
        "[SET COMMENTS]", 
        "这是注释"
    ]
    
    scraper = SmogonScraper()
    set_blocks = scraper._extract_all_set_blocks(test_lines)
    
    print(f"找到 {len(set_blocks)} 个SET块")
    
    for i, block in enumerate(set_blocks):
        print(f"\nSET块 {i+1}:")
        print(f"  SET内容: {block['set_content']}")
        print(f"  注释内容: {block['comments_content']}")
        print(f"  行范围: {block['start_line']}-{block['end_line']}")
        
        # 测试语言判断
        is_en = scraper._is_english_set_block(block)
        is_cn = scraper._is_chinese_set_block(block)
        print(f"  语言判断: 英文={is_en}, 中文={is_cn}")

def test_key_info_extraction():
    """测试关键信息提取"""
    print("\n=== 测试关键信息提取 ===")
    
    test_set_content = [
        "Pokemon: Garchomp",
        "Ability: Rough Skin",
        "Item: Life Orb",
        "Nature: Jolly", 
        "EVs: 252 Atk / 4 HP / 252 Spe",
        "- Dragon Claw",
        "- Earthquake",
        "- Stone Edge",
        "- Swords Dance"
    ]
    
    scraper = SmogonScraper()
    key_info = scraper._extract_set_key_info(test_set_content)
    
    print("提取的关键信息:")
    for key, value in key_info.items():
        print(f"  {key}: {value}")

def test_match_scoring():
    """测试匹配评分"""
    print("\n=== 测试匹配评分 ===")
    
    scraper = SmogonScraper()
    
    # 英文关键信息
    en_key_info = {
        'pokemon': 'Garchomp',
        'ability': 'Rough Skin',
        'item': 'Life Orb',
        'moves': ['Dragon Claw', 'Earthquake', 'Stone Edge', 'Swords Dance'],
        'nature': 'Jolly',
        'evs': '252 Atk / 4 HP / 252 Spe'
    }
    
    # 中文SET内容（匹配）
    cn_set_content_match = [
        "宝可梦: 烈咬陆鲨",
        "特性: 粗糙皮肤", 
        "道具: 生命宝珠",
        "性格: 爽朗",
        "努力值: 252 攻击 / 4 HP / 252 速度",
        "- 龙爪",
        "- 地震",
        "- 尖石攻击",
        "- 剑舞"
    ]
    
    # 中文SET内容（不匹配）
    cn_set_content_no_match = [
        "宝可梦: 多龙巴鲁托",
        "特性: 恒净之躯",
        "道具: 讲究头带",
        "- 龙箭",
        "- 潜灵奇袭"
    ]
    
    score_match = scraper._calculate_set_match_score(en_key_info, cn_set_content_match)
    score_no_match = scraper._calculate_set_match_score(en_key_info, cn_set_content_no_match)
    
    print(f"匹配的中文SET评分: {score_match:.3f}")
    print(f"不匹配的中文SET评分: {score_no_match:.3f}")

def main():
    """主函数"""
    print("SET配对算法测试")
    print("=" * 50)
    
    # 确保输出目录存在
    os.makedirs("scraped_data", exist_ok=True)
    
    # 测试各个组件
    test_set_block_extraction()
    test_key_info_extraction() 
    test_match_scoring()
    
    # 测试完整算法
    pairs = test_set_extraction_algorithm()
    
    # 保存测试结果
    if pairs:
        output_file = "scraped_data/test_set_algorithm.json"
        result = {
            "metadata": {
                "test_type": "SET配对算法测试",
                "total_pairs": len(pairs)
            },
            "translation_pairs": pairs
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print(f"\n测试结果已保存到: {output_file}")
    
    print("\n算法测试完成！")

if __name__ == "__main__":
    main()