#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试保存功能的简单脚本
"""

from smogon_scraper import SmogonScraper

def test_save_functions():
    """测试各种保存功能"""
    print("测试爬虫保存功能...")
    
    # 创建爬虫实例
    scraper = SmogonScraper()
    
    # 添加测试数据
    scraper.translation_pairs = [
        {
            'english': 'Garchomp is a powerful Dragon/Ground-type Pokemon.',
            'chinese': '烈咬陆鲨是一只强大的龙/地面属性宝可梦。',
            'source': '测试数据',
            'type': 'test_pair'
        },
        {
            'english': 'This Pokemon has excellent Attack and Speed stats.',
            'chinese': '这只宝可梦拥有出色的攻击和速度种族值。',
            'source': '测试数据',
            'type': 'test_pair'
        }
    ]
    
    print(f"准备保存 {len(scraper.translation_pairs)} 个翻译对照")
    
    # 测试JSON保存
    print("\n1. 测试JSON格式保存:")
    scraper.save_translations('test_save_json', 'json')
    
    # 测试CSV保存
    print("\n2. 测试CSV格式保存:")
    scraper.save_translations('test_save_csv', 'csv')
    
    # 测试TXT保存
    print("\n3. 测试TXT格式保存:")
    scraper.save_translations('test_save_txt', 'txt')
    
    print("\n保存测试完成！")

if __name__ == "__main__":
    test_save_functions()