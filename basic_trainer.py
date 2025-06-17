#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础翻译学习程序
"""

import json
import os

def load_translation_data():
    """加载翻译数据"""
    try:
        with open('ml_translation_pairs.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('translation_pairs', [])
    except Exception as e:
        print(f"加载数据失败: {e}")
        return []

def analyze_translations(pairs):
    """分析翻译对"""
    print("=== 翻译对学习分析 ===")
    print(f"总翻译对数量: {len(pairs)}")
    
    # 统计不同类型的翻译对
    section_types = {}
    for pair in pairs:
        section_type = pair.get('section_type', 'UNKNOWN')
        section_types[section_type] = section_types.get(section_type, 0) + 1
    
    print("\n按类型分布:")
    for section_type, count in section_types.items():
        print(f"  {section_type}: {count} 个")
    
    # 分析文本长度
    english_lengths = []
    chinese_lengths = []
    
    for pair in pairs:
        english_text = pair.get('english', '')
        chinese_text = pair.get('chinese', '')
        english_lengths.append(len(english_text))
        chinese_lengths.append(len(chinese_text))
    
    if english_lengths and chinese_lengths:
        avg_en_length = sum(english_lengths) / len(english_lengths)
        avg_zh_length = sum(chinese_lengths) / len(chinese_lengths)
        
        print(f"\n文本长度分析:")
        print(f"  英文平均长度: {avg_en_length:.1f} 字符")
        print(f"  中文平均长度: {avg_zh_length:.1f} 字符")
        print(f"  最长英文: {max(english_lengths)} 字符")
        print(f"  最长中文: {max(chinese_lengths)} 字符")

def extract_common_terms(pairs):
    """提取常见术语"""
    print("\n=== 常见术语提取 ===")
    
    # 英文常见词汇
    english_words = {}
    chinese_chars = {}
    
    for pair in pairs:
        english_text = pair.get('english', '').lower()
        chinese_text = pair.get('chinese', '')
        
        # 简单的英文单词提取
        import re
        words = re.findall(r'\b[a-zA-Z]{3,}\b', english_text)
        for word in words:
            english_words[word] = english_words.get(word, 0) + 1
        
        # 中文字符统计
        for char in chinese_text:
            if '\u4e00' <= char <= '\u9fff':  # 中文字符范围
                chinese_chars[char] = chinese_chars.get(char, 0) + 1
    
    # 显示最常见的英文词汇
    print("最常见的英文词汇:")
    sorted_english = sorted(english_words.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_english[:20]:
        print(f"  {word}: {count} 次")
    
    # 显示最常见的中文字符
    print("\n最常见的中文字符:")
    sorted_chinese = sorted(chinese_chars.items(), key=lambda x: x[1], reverse=True)
    for char, count in sorted_chinese[:20]:
        print(f"  {char}: {count} 次")

def create_translation_dictionary(pairs):
    """创建翻译词典"""
    print("\n=== 创建翻译词典 ===")
    
    # 宝可梦专业术语词典
    pokemon_dict = {
        'pokemon': '宝可梦',
        'attack': '攻击',
        'defense': '防御',
        'special': '特殊',
        'speed': '速度',
        'ability': '特性',
        'move': '招式',
        'type': '属性',
        'wall': '盾牌',
        'sweeper': '清场手',
        'setup': '强化',
        'bulk': '耐久',
        'coverage': '打击面',
        'utility': '功能性',
        'pivot': '中转',
        'hazards': '场地危险',
        'stealth rock': '隐形岩',
        'spikes': '撒菱',
        'boots': '厚底靴',
        'leftovers': '吃剩的东西',
        'choice': '讲究',
        'scarf': '围巾',
        'tera': '太晶',
        'mega': '超级'
    }
    
    print(f"基础宝可梦术语词典: {len(pokemon_dict)} 个术语")
    
    # 从翻译对中学习新的术语对应关系
    learned_terms = {}
    
    for pair in pairs:
        english_text = pair.get('english', '').lower()
        chinese_text = pair.get('chinese', '')
        
        # 查找英文术语在中文中的对应
        for en_term, zh_term in pokemon_dict.items():
            if en_term in english_text and zh_term in chinese_text:
                learned_terms[en_term] = zh_term
    
    print(f"从翻译对中确认的术语: {len(learned_terms)} 个")
    
    return {**pokemon_dict, **learned_terms}

def demonstrate_translation(translation_dict):
    """演示翻译功能"""
    print("\n=== 翻译演示 ===")
    
    test_phrases = [
        "Pokemon with high attack stats",
        "defensive wall pokemon",
        "special attacker with good coverage",
        "stealth rock hazards",
        "choice scarf revenge killer",
        "mega evolution setup"
    ]
    
    for phrase in test_phrases:
        print(f"\n英文: {phrase}")
        
        # 简单的术语替换翻译
        translated = phrase.lower()
        found_terms = []
        
        for en_term, zh_term in translation_dict.items():
            if en_term in translated:
                translated = translated.replace(en_term, zh_term)
                found_terms.append(f"{en_term} -> {zh_term}")
        
        if found_terms:
            print(f"识别术语: {', '.join(found_terms)}")
            print(f"翻译结果: {translated}")
        else:
            print("未识别到已知术语")

def save_learning_results(translation_dict, pairs):
    """保存学习结果"""
    results = {
        'learning_date': '2025-06-17',
        'total_pairs': len(pairs),
        'translation_dictionary': translation_dict,
        'statistics': {
            'english_terms': len([k for k in translation_dict.keys() if k.isascii()]),
            'chinese_terms': len([v for v in translation_dict.values() if not v.isascii()])
        }
    }
    
    try:
        with open('translation_learning_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n学习结果已保存到: translation_learning_results.json")
    except Exception as e:
        print(f"保存结果失败: {e}")

def main():
    """主函数"""
    print("开始翻译对学习...")
    
    # 1. 加载数据
    pairs = load_translation_data()
    if not pairs:
        print("无法加载翻译数据")
        return
    
    # 2. 分析翻译对
    analyze_translations(pairs)
    
    # 3. 提取常见术语
    extract_common_terms(pairs)
    
    # 4. 创建翻译词典
    translation_dict = create_translation_dictionary(pairs)
    
    # 5. 演示翻译
    demonstrate_translation(translation_dict)
    
    # 6. 保存学习结果
    save_learning_results(translation_dict, pairs)
    
    print("\n翻译对学习完成!")

if __name__ == "__main__":
    main()