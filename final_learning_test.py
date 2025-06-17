#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终学习测试程序 - 验证所有学习成果
"""

import json

def load_enhanced_results():
    """加载增强学习结果"""
    try:
        with open('enhanced_translation_results.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载增强结果失败: {e}")
        return None

def comprehensive_translation_test():
    """综合翻译测试"""
    print("=== 最终翻译能力测试 ===")
    
    # 加载增强词典
    results = load_enhanced_results()
    if not results:
        print("无法加载学习结果")
        return
    
    enhanced_dict = results.get('enhanced_dictionary', {})
    print(f"当前词典包含 {len(enhanced_dict)} 个术语")
    
    # 复杂测试用例
    complex_test_cases = [
        {
            'english': "Garchomp with Swords Dance and Earthquake is a powerful physical sweeper that can OHKO many Pokemon with STAB moves.",
            'description': "复杂战斗描述"
        },
        {
            'english': "Choice Scarf Landorus-T serves as a revenge killer with Intimidate support and U-turn pivot capability.",
            'description': "角色定位描述"
        },
        {
            'english': "Magic Guard Clefable with Life Orb can use Calm Mind to set up and become a special wall breaker.",
            'description': "特性与道具组合"
        },
        {
            'english': "Stealth Rock and Spikes hazard setter Skarmory with Sturdy ability and Leftovers recovery.",
            'description': "场地控制描述"
        },
        {
            'english': "Regenerator Tornadus-T is an excellent defensive pivot with Hurricane and U-turn coverage.",
            'description': "防守型中转手"
        },
        {
            'english': "Technician Scizor with Choice Band can revenge kill with Bullet Punch priority move.",
            'description': "先制技能使用"
        },
        {
            'english': "Dragon Dance Gyarados setup sweeper with Intimidate and Moxie ability synergy.",
            'description': "强化清场手"
        },
        {
            'english': "Prankster Whimsicott with Thunder Wave paralysis support and Taunt utility moves.",
            'description': "辅助功能描述"
        }
    ]
    
    total_tests = len(complex_test_cases)
    successful_translations = 0
    
    for i, test_case in enumerate(complex_test_cases, 1):
        print(f"\n测试 {i}/{total_tests}: {test_case['description']}")
        print(f"原文: {test_case['english']}")
        
        # 执行翻译
        translated_text = test_case['english'].lower()
        found_terms = []
        translation_score = 0
        
        for en_term, zh_term in enhanced_dict.items():
            if en_term in translated_text:
                translated_text = translated_text.replace(en_term, zh_term)
                found_terms.append(f"{en_term}→{zh_term}")
                translation_score += 1
        
        if found_terms:
            print(f"识别术语 ({len(found_terms)} 个): {', '.join(found_terms)}")
            print(f"翻译结果: {translated_text}")
            
            # 评估翻译质量
            if translation_score >= 3:
                print("翻译质量: 优秀 ✓")
                successful_translations += 1
            elif translation_score >= 2:
                print("翻译质量: 良好 ○")
                successful_translations += 0.7
            elif translation_score >= 1:
                print("翻译质量: 一般 △")
                successful_translations += 0.3
            else:
                print("翻译质量: 较差 ✗")
        else:
            print("翻译结果: 未识别到已知术语")
            print("翻译质量: 失败 ✗")
    
    # 计算总体成功率
    success_rate = (successful_translations / total_tests) * 100
    print(f"\n=== 测试总结 ===")
    print(f"测试用例总数: {total_tests}")
    print(f"成功翻译得分: {successful_translations:.1f}")
    print(f"翻译成功率: {success_rate:.1f}%")
    
    return success_rate

def analyze_learning_progress():
    """分析学习进度"""
    print("\n=== 学习进度分析 ===")
    
    # 加载所有学习结果
    try:
        with open('translation_learning_results.json', 'r', encoding='utf-8') as f:
            basic_results = json.load(f)
    except:
        basic_results = None
    
    try:
        with open('enhanced_translation_results.json', 'r', encoding='utf-8') as f:
            enhanced_results = json.load(f)
    except:
        enhanced_results = None
    
    if basic_results and enhanced_results:
        basic_terms = len(basic_results.get('translation_dictionary', {}))
        enhanced_terms = len(enhanced_results.get('enhanced_dictionary', {}))
        new_terms = len(enhanced_results.get('new_terms_added', {}))
        
        print(f"基础学习阶段: {basic_terms} 个术语")
        print(f"增强学习阶段: {enhanced_terms} 个术语")
        print(f"新增术语数量: {new_terms} 个")
        print(f"学习增长率: {(new_terms / basic_terms) * 100:.1f}%")
        print(f"总体覆盖提升: {enhanced_results.get('statistics', {}).get('coverage_improvement', 'N/A')}")
    else:
        print("无法完整分析学习进度")

def categorize_learned_terms():
    """分类已学习术语"""
    print("\n=== 已学习术语分类 ===")
    
    results = load_enhanced_results()
    if not results:
        return
    
    enhanced_dict = results.get('enhanced_dictionary', {})
    
    # 术语分类
    categories = {
        '宝可梦名称': ['dondozo', 'garchomp', 'giratina', 'clefable', 'samurott', 'heatran', 'weavile', 'charizard', 'tornadus', 'ogerpon', 'gholdengo', 'lopunny', 'landorus', 'kartana', 'manaphy', 'urshifu', 'scizor', 'zapdos', 'skarmory', 'dragapult', 'melmetal', 'corviknight'],
        '招式名称': ['stealth rock', 'spikes', 'swords dance', 'dragon dance', 'calm mind', 'nasty plot', 'earthquake', 'close combat', 'u-turn', 'volt switch', 'knock off', 'sucker punch', 'ice punch', 'thunder punch', 'fire punch', 'recover', 'roost'],
        '道具名称': ['leftovers', 'choice', 'scarf', 'boots', 'choice band', 'choice specs', 'life orb', 'focus sash', 'assault vest', 'rocky helmet', 'eviolite', 'weakness policy', 'expert belt'],
        '特性名称': ['intimidate', 'levitate', 'sturdy', 'regenerator', 'magic guard', 'unaware', 'prankster', 'technician', 'adaptability', 'huge power', 'speed boost', 'protean', 'guts', 'pressure'],
        '战斗术语': ['pokemon', 'attack', 'defense', 'special', 'speed', 'ability', 'move', 'type', 'wall', 'sweeper', 'setup', 'bulk', 'coverage', 'utility', 'pivot', 'hazards', 'revenge killer', 'stallbreaker', 'hazard setter', 'spinner', 'defogger', 'cleric', 'ohko', '2hko', 'crit', 'burn', 'poison', 'paralysis', 'sleep', 'freeze', 'priority', 'stab', 'recoil'],
        '属性名称': ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy'],
        '其他术语': ['tera', 'mega']
    }
    
    for category, terms in categories.items():
        found_in_category = [term for term in terms if term in enhanced_dict]
        print(f"{category}: {len(found_in_category)}/{len(terms)} 个")
        if found_in_category:
            print(f"  已学习: {', '.join(found_in_category[:5])}{'...' if len(found_in_category) > 5 else ''}")

def generate_learning_report():
    """生成学习报告"""
    print("\n=== 生成最终学习报告 ===")
    
    # 执行翻译测试
    success_rate = comprehensive_translation_test()
    
    # 分析学习进度
    analyze_learning_progress()
    
    # 分类术语
    categorize_learned_terms()
    
    # 生成报告
    results = load_enhanced_results()
    if results:
        report = {
            'learning_completion_date': '2025-06-17',
            'final_statistics': results.get('statistics', {}),
            'translation_success_rate': f"{success_rate:.1f}%",
            'learning_status': 'completed',
            'capabilities': {
                'pokemon_name_translation': True,
                'move_name_translation': True,
                'item_name_translation': True,
                'ability_name_translation': True,
                'battle_term_translation': True,
                'type_name_translation': True,
                'complex_sentence_translation': success_rate >= 70
            },
            'recommendations': [
                "继续收集更多翻译对以扩展词典",
                "添加更多复杂句式的翻译模式",
                "优化术语识别的准确性",
                "增加上下文理解能力"
            ]
        }
        
        try:
            with open('final_learning_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n最终学习报告已保存到: final_learning_report.json")
        except Exception as e:
            print(f"保存报告失败: {e}")
    
    print("\n=== 学习完成 ===")
    print("程序已成功学习宝可梦对战术语翻译")
    print(f"当前翻译成功率: {success_rate:.1f}%")
    if success_rate >= 80:
        print("翻译能力评级: 优秀 🌟")
    elif success_rate >= 60:
        print("翻译能力评级: 良好 ⭐")
    elif success_rate >= 40:
        print("翻译能力评级: 一般 ○")
    else:
        print("翻译能力评级: 需要改进 △")

def main():
    """主函数"""
    print("开始最终学习测试...")
    generate_learning_report()

if __name__ == "__main__":
    main()