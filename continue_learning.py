#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
继续学习程序 - 扩展翻译词典
"""

import json

def load_existing_results():
    """加载现有学习结果"""
    try:
        with open('translation_learning_results.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def load_translation_pairs():
    """加载翻译对数据"""
    try:
        with open('ml_translation_pairs.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('translation_pairs', [])
    except:
        return []

def extract_new_terms(pairs, existing_dict):
    """从翻译对中提取新术语"""
    print("=== 提取新术语 ===")
    
    # 扩展的术语库
    extended_terms = {
        # 宝可梦名称
        'dondozo': '吃吼霸',
        'garchomp': '烈咬陆鲨',
        'giratina': '骑拉帝纳',
        'clefable': '皮可西',
        'samurott': '大剑鬼',
        'heatran': '席多蓝恩',
        'weavile': '玛狃拉',
        'charizard': '喷火龙',
        'tornadus': '龙卷云',
        'ogerpon': '厄诡椪',
        'gholdengo': '赛富豪',
        'lopunny': '长耳兔',
        'landorus': '土地云',
        'kartana': '纸御剑',
        'manaphy': '玛纳霏',
        'urshifu': '武道熊师',
        'tapu koko': '卡璞·鸣鸣',
        'scizor': '巨钳螳螂',
        'zapdos': '闪电鸟',
        'skarmory': '盔甲鸟',
        'dragapult': '多龙巴鲁托',
        'melmetal': '美录梅塔',
        'corviknight': '钢铠鸦',
        
        # 招式名称
        'swords dance': '剑舞',
        'dragon dance': '龙之舞',
        'calm mind': '冥想',
        'nasty plot': '诡计',
        'earthquake': '地震',
        'close combat': '近身战',
        'u-turn': 'U型回转',
        'volt switch': '伏特替换',
        'knock off': '拍落',
        'sucker punch': '突袭',
        'ice punch': '冰冻拳',
        'thunder punch': '雷电拳',
        'fire punch': '火焰拳',
        'recover': '自我再生',
        'roost': '羽栖',
        
        # 道具名称
        'choice band': '讲究头带',
        'choice specs': '讲究眼镜',
        'life orb': '生命宝珠',
        'focus sash': '气势头带',
        'assault vest': '突击背心',
        'rocky helmet': '凸凹头盔',
        'eviolite': '进化奇石',
        'weakness policy': '弱点保险',
        'expert belt': '专爱带',
        
        # 特性名称
        'intimidate': '威吓',
        'levitate': '飘浮',
        'sturdy': '结实',
        'regenerator': '再生力',
        'magic guard': '魔法防守',
        'unaware': '天然',
        'prankster': '恶作剧之心',
        'technician': '技术高手',
        'adaptability': '适应力',
        'huge power': '大力士',
        'speed boost': '加速',
        'protean': '变幻自如',
        'guts': '毅力',
        'pressure': '压迫感',
        
        # 战斗术语
        'revenge killer': '报仇杀手',
        'stallbreaker': '破盾手',
        'hazard setter': '撒钉手',
        'spinner': '清场者',
        'defogger': '除雾者',
        'cleric': '奶妈',
        'ohko': '一击必杀',
        '2hko': '二回合击杀',
        'crit': '会心一击',
        'burn': '烧伤',
        'poison': '中毒',
        'paralysis': '麻痹',
        'sleep': '睡眠',
        'freeze': '冰冻',
        'priority': '先制',
        'stab': '本系加成',
        'recoil': '反作用力',
        
        # 属性名称
        'normal': '一般',
        'fire': '火',
        'water': '水',
        'electric': '电',
        'grass': '草',
        'ice': '冰',
        'fighting': '格斗',
        'poison': '毒',
        'ground': '地面',
        'flying': '飞行',
        'psychic': '超能力',
        'bug': '虫',
        'rock': '岩石',
        'ghost': '幽灵',
        'dragon': '龙',
        'dark': '恶',
        'steel': '钢',
        'fairy': '妖精'
    }
    
    # 检查哪些术语在翻译对中出现
    found_terms = {}
    new_terms = {}
    
    for en_term, zh_term in extended_terms.items():
        # 检查是否已存在
        if en_term in existing_dict:
            found_terms[en_term] = zh_term
        else:
            # 检查是否在翻译对中出现
            for pair in pairs:
                english_text = pair.get('english', '').lower()
                chinese_text = pair.get('chinese', '')
                
                if en_term in english_text and zh_term in chinese_text:
                    new_terms[en_term] = zh_term
                    break
    
    print(f"已有术语确认: {len(found_terms)} 个")
    print(f"新发现术语: {len(new_terms)} 个")
    
    if new_terms:
        print("\n新术语列表:")
        for en_term, zh_term in new_terms.items():
            print(f"  {en_term} -> {zh_term}")
    
    return new_terms

def analyze_text_patterns(pairs):
    """分析文本模式"""
    print("\n=== 分析文本模式 ===")
    
    # 统计常见词汇
    english_words = {}
    chinese_chars = {}
    
    for pair in pairs:
        english_text = pair.get('english', '').lower()
        chinese_text = pair.get('chinese', '')
        
        # 英文单词统计
        import re
        words = re.findall(r'\b[a-zA-Z]{2,}\b', english_text)
        for word in words:
            english_words[word] = english_words.get(word, 0) + 1
        
        # 中文字符统计
        for char in chinese_text:
            if '\u4e00' <= char <= '\u9fff':
                chinese_chars[char] = chinese_chars.get(char, 0) + 1
    
    # 显示高频词汇
    print("高频英文词汇 (前15个):")
    sorted_english = sorted(english_words.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_english[:15]:
        if count >= 3:  # 至少出现3次
            print(f"  {word}: {count} 次")
    
    print("\n高频中文字符 (前15个):")
    sorted_chinese = sorted(chinese_chars.items(), key=lambda x: x[1], reverse=True)
    for char, count in sorted_chinese[:15]:
        if count >= 3:  # 至少出现3次
            print(f"  {char}: {count} 次")
    
    return {
        'high_freq_english': {word: count for word, count in sorted_english[:15] if count >= 3},
        'high_freq_chinese': {char: count for char, count in sorted_chinese[:15] if count >= 3}
    }

def create_enhanced_dictionary(existing_dict, new_terms):
    """创建增强词典"""
    print("\n=== 创建增强词典 ===")
    
    enhanced_dict = {**existing_dict, **new_terms}
    
    print(f"原有术语: {len(existing_dict)} 个")
    print(f"新增术语: {len(new_terms)} 个")
    print(f"总计术语: {len(enhanced_dict)} 个")
    
    return enhanced_dict

def test_enhanced_translation(enhanced_dict):
    """测试增强翻译"""
    print("\n=== 测试增强翻译 ===")
    
    test_cases = [
        "Garchomp with Swords Dance is a powerful sweeper",
        "Intimidate Landorus-T with U-turn pivot",
        "Choice Scarf revenge killer Kartana",
        "Magic Guard Clefable with Life Orb",
        "Stealth Rock and Spikes hazard setter",
        "Dragon Dance Gyarados setup sweeper",
        "Regenerator Tornadus-T defensive pivot",
        "STAB Close Combat from Urshifu"
    ]
    
    for test_text in test_cases:
        print(f"\n原文: {test_text}")
        translated = test_text.lower()
        found_terms = []
        
        for en_term, zh_term in enhanced_dict.items():
            if en_term in translated:
                translated = translated.replace(en_term, zh_term)
                found_terms.append(f"{en_term}→{zh_term}")
        
        if found_terms:
            print(f"识别: {', '.join(found_terms)}")
            print(f"翻译: {translated}")
        else:
            print("翻译: 未识别到已知术语")

def save_enhanced_results(enhanced_dict, new_terms, patterns, pairs):
    """保存增强学习结果"""
    results = {
        'learning_date': '2025-06-17',
        'learning_type': 'enhanced_continuation',
        'total_pairs': len(pairs),
        'enhanced_dictionary': enhanced_dict,
        'new_terms_added': new_terms,
        'text_patterns': patterns,
        'statistics': {
            'total_terms': len(enhanced_dict),
            'new_terms': len(new_terms),
            'coverage_improvement': f"{len(new_terms) / len(enhanced_dict) * 100:.1f}%"
        }
    }
    
    try:
        with open('enhanced_translation_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n增强学习结果已保存到: enhanced_translation_results.json")
        return True
    except Exception as e:
        print(f"保存结果失败: {e}")
        return False

def main():
    """主函数"""
    print("开始继续学习...")
    
    # 1. 加载现有结果
    existing_results = load_existing_results()
    if not existing_results:
        print("未找到现有学习结果")
        return
    
    existing_dict = existing_results.get('translation_dictionary', {})
    print(f"加载现有词典: {len(existing_dict)} 个术语")
    
    # 2. 加载翻译对
    pairs = load_translation_pairs()
    if not pairs:
        print("无法加载翻译对数据")
        return
    
    print(f"加载翻译对: {len(pairs)} 个")
    
    # 3. 提取新术语
    new_terms = extract_new_terms(pairs, existing_dict)
    
    # 4. 分析文本模式
    patterns = analyze_text_patterns(pairs)
    
    # 5. 创建增强词典
    enhanced_dict = create_enhanced_dictionary(existing_dict, new_terms)
    
    # 6. 测试增强翻译
    test_enhanced_translation(enhanced_dict)
    
    # 7. 保存结果
    if save_enhanced_results(enhanced_dict, new_terms, patterns, pairs):
        print("\n继续学习完成!")
        print(f"词典从 {len(existing_dict)} 个术语扩展到 {len(enhanced_dict)} 个术语")
        print(f"新增 {len(new_terms)} 个术语，提升覆盖率 {len(new_terms) / len(enhanced_dict) * 100:.1f}%")
    else:
        print("\n学习过程中出现错误")

if __name__ == "__main__":
    main()