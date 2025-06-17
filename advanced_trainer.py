#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级翻译学习程序 - 深度分析翻译对
"""

import json
import re
from collections import defaultdict, Counter

def load_translation_data():
    """加载翻译数据"""
    try:
        with open('ml_translation_pairs.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('translation_pairs', [])
    except Exception as e:
        print(f"加载数据失败: {e}")
        return []

def extract_pokemon_names(pairs):
    """提取宝可梦名称对应关系"""
    print("=== 提取宝可梦名称 ===")
    
    # 常见宝可梦名称映射
    pokemon_names = {
        'dondozo': '吃吼霸',
        'samurott': '大剑鬼',
        'garchomp': '烈咬陆鲨',
        'heatran': '席多蓝恩',
        'giratina': '骑拉帝纳',
        'clefable': '皮可西',
        'skarmory': '盔甲鸟',
        'weavile': '玛狃拉',
        'charizard': '喷火龙',
        'tornadus': '龙卷云',
        'ogerpon': '厄诡椪',
        'gholdengo': '赛富豪',
        'lopunny': '长耳兔',
        'landorus': '土地云',
        'crobat': '叉字蝠',
        'kartana': '纸御剑',
        'manaphy': '玛纳霏',
        'urshifu': '武道熊师',
        'tapu koko': '卡璞·鸣鸣',
        'dragapult': '多龙巴鲁托',
        'scizor': '巨钳螳螂',
        'zapdos': '闪电鸟',
        'melmetal': '美录梅塔',
        'corviknight': '钢铠鸦',
        'kartana': '纸御剑'
    }
    
    # 从翻译对中学习新的宝可梦名称
    learned_names = {}
    
    for pair in pairs:
        english_text = pair.get('english', '').lower()
        chinese_text = pair.get('chinese', '')
        
        # 查找已知宝可梦名称
        for en_name, zh_name in pokemon_names.items():
            if en_name in english_text and zh_name in chinese_text:
                learned_names[en_name] = zh_name
    
    print(f"识别到的宝可梦名称: {len(learned_names)} 个")
    for en_name, zh_name in learned_names.items():
        print(f"  {en_name} -> {zh_name}")
    
    return {**pokemon_names, **learned_names}

def extract_move_names(pairs):
    """提取招式名称"""
    print("\n=== 提取招式名称 ===")
    
    move_names = {
        'stealth rock': '隐形岩',
        'spikes': '撒菱',
        'toxic spikes': '毒菱',
        'sticky web': '黏黏网',
        'swords dance': '剑舞',
        'dragon dance': '龙之舞',
        'calm mind': '冥想',
        'nasty plot': '诡计',
        'bulk up': '健美',
        'iron defense': '铁壁',
        'recover': '自我再生',
        'roost': '羽栖',
        'u-turn': 'U型回转',
        'volt switch': '伏特替换',
        'flip turn': '快速折返',
        'earthquake': '地震',
        'close combat': '近身战',
        'flare blitz': '闪焰冲锋',
        'ice punch': '冰冻拳',
        'thunder punch': '雷电拳',
        'fire punch': '火焰拳',
        'knock off': '拍落',
        'sucker punch': '突袭',
        'extreme speed': '神速',
        'bullet punch': '子弹拳',
        'ice shard': '冰砾',
        'aqua jet': '水流喷射'
    }
    
    learned_moves = {}
    
    for pair in pairs:
        english_text = pair.get('english', '').lower()
        chinese_text = pair.get('chinese', '')
        
        for en_move, zh_move in move_names.items():
            if en_move in english_text and zh_move in chinese_text:
                learned_moves[en_move] = zh_move
    
    print(f"识别到的招式名称: {len(learned_moves)} 个")
    for en_move, zh_move in learned_moves.items():
        print(f"  {en_move} -> {zh_move}")
    
    return {**move_names, **learned_moves}

def extract_item_names(pairs):
    """提取道具名称"""
    print("\n=== 提取道具名称 ===")
    
    item_names = {
        'leftovers': '吃剩的东西',
        'choice band': '讲究头带',
        'choice scarf': '讲究围巾',
        'choice specs': '讲究眼镜',
        'life orb': '生命宝珠',
        'focus sash': '气势头带',
        'assault vest': '突击背心',
        'heavy-duty boots': '厚底靴',
        'rocky helmet': '凸凹头盔',
        'eviolite': '进化奇石',
        'weakness policy': '弱点保险',
        'white herb': '白色香草',
        'mental herb': '心灵香草',
        'power herb': '强力香草',
        'expert belt': '专爱带',
        'muscle band': '力量头带',
        'wise glasses': '博识眼镜',
        'scope lens': '焦点镜',
        'razor claw': '锐利爪',
        'king\'s rock': '王者之证',
        'bright powder': '光粉',
        'lax incense': '悠闲薰香'
    }
    
    learned_items = {}
    
    for pair in pairs:
        english_text = pair.get('english', '').lower()
        chinese_text = pair.get('chinese', '')
        
        for en_item, zh_item in item_names.items():
            if en_item in english_text and zh_item in chinese_text:
                learned_items[en_item] = zh_item
    
    print(f"识别到的道具名称: {len(learned_items)} 个")
    for en_item, zh_item in learned_items.items():
        print(f"  {en_item} -> {zh_item}")
    
    return {**item_names, **learned_items}

def extract_ability_names(pairs):
    """提取特性名称"""
    print("\n=== 提取特性名称 ===")
    
    ability_names = {
        'intimidate': '威吓',
        'levitate': '飘浮',
        'sturdy': '结实',
        'multiscale': '多重鳞片',
        'regenerator': '再生力',
        'magic guard': '魔法防守',
        'unaware': '天然',
        'prankster': '恶作剧之心',
        'technician': '技术高手',
        'adaptability': '适应力',
        'huge power': '大力士',
        'pure power': '纯粹之力',
        'speed boost': '加速',
        'protean': '变幻自如',
        'libero': '自由者',
        'guts': '毅力',
        'marvel scale': '神奇鳞片',
        'flame body': '火焰之躯',
        'static': '静电',
        'poison point': '毒刺',
        'rough skin': '粗糙皮肤',
        'iron barbs': '铁刺',
        'pressure': '压迫感',
        'sand stream': '扬沙',
        'drought': '日照',
        'drizzle': '降雨',
        'snow warning': '降雪'
    }
    
    learned_abilities = {}
    
    for pair in pairs:
        english_text = pair.get('english', '').lower()
        chinese_text = pair.get('chinese', '')
        
        for en_ability, zh_ability in ability_names.items():
            if en_ability in english_text and zh_ability in chinese_text:
                learned_abilities[en_ability] = zh_ability
    
    print(f"识别到的特性名称: {len(learned_abilities)} 个")
    for en_ability, zh_ability in learned_abilities.items():
        print(f"  {en_ability} -> {zh_ability}")
    
    return {**ability_names, **learned_abilities}

def analyze_translation_patterns(pairs):
    """分析翻译模式"""
    print("\n=== 分析翻译模式 ===")
    
    patterns = {
        'stat_terms': {
            'hp': 'HP',
            'attack': '攻击',
            'defense': '防御',
            'special attack': '特攻',
            'special defense': '特防',
            'speed': '速度',
            'atk': '攻击',
            'def': '防御',
            'spa': '特攻',
            'spd': '特防',
            'spe': '速度'
        },
        'role_terms': {
            'sweeper': '清场手',
            'wall': '盾牌',
            'tank': '坦克',
            'pivot': '中转',
            'revenge killer': '报仇杀手',
            'setup sweeper': '强化清场手',
            'stallbreaker': '破盾手',
            'hazard setter': '撒钉手',
            'spinner': '清场者',
            'defogger': '除雾者',
            'cleric': '奶妈',
            'support': '辅助'
        },
        'battle_terms': {
            'ohko': '一击必杀',
            '2hko': '二回合击杀',
            'crit': '会心一击',
            'flinch': '畏缩',
            'burn': '烧伤',
            'poison': '中毒',
            'paralysis': '麻痹',
            'sleep': '睡眠',
            'freeze': '冰冻',
            'confusion': '混乱',
            'recoil': '反作用力',
            'priority': '先制',
            'stab': '本系加成'
        }
    }
    
    learned_patterns = defaultdict(dict)
    
    for category, terms in patterns.items():
        for pair in pairs:
            english_text = pair.get('english', '').lower()
            chinese_text = pair.get('chinese', '')
            
            for en_term, zh_term in terms.items():
                if en_term in english_text and zh_term in chinese_text:
                    learned_patterns[category][en_term] = zh_term
    
    for category, terms in learned_patterns.items():
        print(f"\n{category} ({len(terms)} 个):")
        for en_term, zh_term in terms.items():
            print(f"  {en_term} -> {zh_term}")
    
    return dict(learned_patterns)

def create_comprehensive_dictionary(pokemon_names, move_names, item_names, ability_names, patterns):
    """创建综合词典"""
    print("\n=== 创建综合翻译词典 ===")
    
    comprehensive_dict = {
        'pokemon_names': pokemon_names,
        'move_names': move_names,
        'item_names': item_names,
        'ability_names': ability_names,
        'battle_patterns': patterns
    }
    
    # 统计总术语数
    total_terms = 0
    for category, terms in comprehensive_dict.items():
        if isinstance(terms, dict):
            if category == 'battle_patterns':
                for sub_category, sub_terms in terms.items():
                    total_terms += len(sub_terms)
            else:
                total_terms += len(terms)
    
    print(f"综合词典包含 {total_terms} 个术语")
    print(f"  宝可梦名称: {len(pokemon_names)} 个")
    print(f"  招式名称: {len(move_names)} 个")
    print(f"  道具名称: {len(item_names)} 个")
    print(f"  特性名称: {len(ability_names)} 个")
    
    pattern_count = sum(len(terms) for terms in patterns.values())
    print(f"  战斗术语: {pattern_count} 个")
    
    return comprehensive_dict

def advanced_translation_demo(comprehensive_dict):
    """高级翻译演示"""
    print("\n=== 高级翻译演示 ===")
    
    test_sentences = [
        "Garchomp with Swords Dance and Earthquake",
        "Clefable is a great special wall with Magic Guard",
        "Choice Scarf Landorus-T for revenge killing",
        "Stealth Rock setter with Leftovers",
        "Intimidate Gyarados with Dragon Dance setup",
        "Life Orb Kartana with Leaf Blade coverage"
    ]
    
    for sentence in test_sentences:
        print(f"\n原文: {sentence}")
        translated = sentence.lower()
        found_terms = []
        
        # 翻译各类术语
        for category, terms in comprehensive_dict.items():
            if category == 'battle_patterns':
                for sub_category, sub_terms in terms.items():
                    for en_term, zh_term in sub_terms.items():
                        if en_term in translated:
                            translated = translated.replace(en_term, zh_term)
                            found_terms.append(f"{en_term}→{zh_term}")
            else:
                for en_term, zh_term in terms.items():
                    if en_term in translated:
                        translated = translated.replace(en_term, zh_term)
                        found_terms.append(f"{en_term}→{zh_term}")
        
        if found_terms:
            print(f"识别术语: {', '.join(found_terms)}")
            print(f"翻译结果: {translated}")
        else:
            print("未识别到已知术语")

def save_advanced_results(comprehensive_dict, pairs):
    """保存高级学习结果"""
    results = {
        'learning_date': '2025-06-17',
        'learning_type': 'advanced',
        'total_pairs': len(pairs),
        'comprehensive_dictionary': comprehensive_dict,
        'statistics': {
            'pokemon_names': len(comprehensive_dict['pokemon_names']),
            'move_names': len(comprehensive_dict['move_names']),
            'item_names': len(comprehensive_dict['item_names']),
            'ability_names': len(comprehensive_dict['ability_names']),
            'battle_patterns': sum(len(terms) for terms in comprehensive_dict['battle_patterns'].values())
        }
    }
    
    try:
        with open('advanced_translation_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n高级学习结果已保存到: advanced_translation_results.json")
    except Exception as e:
        print(f"保存结果失败: {e}")

def main():
    """主函数"""
    print("开始高级翻译学习...")
    
    # 1. 加载数据
    pairs = load_translation_data()
    if not pairs:
        print("无法加载翻译数据")
        return
    
    print(f"加载了 {len(pairs)} 个翻译对")
    
    # 2. 提取各类术语
    pokemon_names = extract_pokemon_names(pairs)
    move_names = extract_move_names(pairs)
    item_names = extract_item_names(pairs)
    ability_names = extract_ability_names(pairs)
    
    # 3. 分析翻译模式
    patterns = analyze_translation_patterns(pairs)
    
    # 4. 创建综合词典
    comprehensive_dict = create_comprehensive_dictionary(
        pokemon_names, move_names, item_names, ability_names, patterns
    )
    
    # 5. 高级翻译演示
    advanced_translation_demo(comprehensive_dict)
    
    # 6. 保存结果
    save_advanced_results(comprehensive_dict, pairs)
    
    print("\n高级翻译学习完成!")

if __name__ == "__main__":
    main()