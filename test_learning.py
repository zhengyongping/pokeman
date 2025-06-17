#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试翻译学习结果
"""

import json

def test_learning_results():
    """测试学习结果"""
    try:
        # 读取学习结果
        with open('translation_learning_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        print("=== 翻译学习结果测试 ===")
        print(f"学习日期: {results['learning_date']}")
        print(f"总翻译对数: {results['total_pairs']}")
        print(f"英文术语数: {results['statistics']['english_terms']}")
        print(f"中文术语数: {results['statistics']['chinese_terms']}")
        
        # 测试翻译词典
        translation_dict = results['translation_dictionary']
        print(f"\n翻译词典包含 {len(translation_dict)} 个术语对:")
        
        for en_term, zh_term in list(translation_dict.items())[:10]:
            print(f"  {en_term} -> {zh_term}")
        
        if len(translation_dict) > 10:
            print(f"  ... 还有 {len(translation_dict) - 10} 个术语")
        
        # 简单翻译测试
        print("\n=== 翻译测试 ===")
        test_phrases = [
            "Pokemon with high attack",
            "defensive wall",
            "special coverage",
            "choice scarf",
            "stealth rock"
        ]
        
        for phrase in test_phrases:
            translated = phrase.lower()
            found_terms = []
            
            for en_term, zh_term in translation_dict.items():
                if en_term in translated:
                    translated = translated.replace(en_term, zh_term)
                    found_terms.append(f"{en_term}→{zh_term}")
            
            print(f"原文: {phrase}")
            if found_terms:
                print(f"识别: {', '.join(found_terms)}")
                print(f"翻译: {translated}")
            else:
                print(f"翻译: 未识别到已知术语")
            print()
        
        print("学习结果测试完成!")
        return True
        
    except FileNotFoundError:
        print("错误: 未找到学习结果文件 translation_learning_results.json")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False

if __name__ == "__main__":
    test_learning_results()