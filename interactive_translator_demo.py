# -*- coding: utf-8 -*-
"""
交互式翻译器演示 - 支持用户输入任意文本进行翻译
"""

import json
from final_translator import FinalTranslator

def interactive_demo():
    """交互式翻译演示"""
    print("=== 宝可梦对战术语翻译器 ===")
    print("支持长文本完全翻译")
    print("输入 'quit' 或 'exit' 退出程序")
    print("输入 'help' 查看帮助信息")
    print("=" * 50)
    
    # 初始化翻译器
    translator = FinalTranslator()
    
    print(f"翻译器已加载:")
    print(f"  专业术语: {len(translator.dictionary)} 个")
    print(f"  复合术语: {len(translator.compound_terms)} 个")
    print(f"  常用词汇: {len(translator.common_words)} 个")
    print(f"  句型模式: {len(translator.sentence_patterns)} 个")
    print()
    
    # 示例文本
    examples = [
        "Garchomp is a great sweeper with Swords Dance.",
        "This Heatran set is designed to provide special attack coverage.",
        "Weavile can OHKO Garchomp with Ice Punch after Stealth Rock damage.",
        "Clefable with Magic Guard ability can be used as a special wall.",
        "This team focuses on offensive pressure with multiple sweepers."
    ]
    
    session_results = []
    
    while True:
        try:
            user_input = input("请输入要翻译的英文文本: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("感谢使用翻译器！")
                break
            elif user_input.lower() in ['help', '帮助']:
                print("\n=== 帮助信息 ===")
                print("1. 输入任意英文文本进行翻译")
                print("2. 支持单句和多句翻译")
                print("3. 输入 'examples' 查看示例")
                print("4. 输入 'stats' 查看本次会话统计")
                print("5. 输入 'quit' 退出程序")
                print("=" * 30)
                continue
            elif user_input.lower() in ['examples', '示例']:
                print("\n=== 翻译示例 ===")
                for i, example in enumerate(examples, 1):
                    translated = translator.translate_text(example)
                    print(f"{i}. 原文: {example}")
                    print(f"   译文: {translated}")
                    print()
                continue
            elif user_input.lower() in ['stats', '统计']:
                if session_results:
                    print("\n=== 本次会话统计 ===")
                    total_coverage = sum(r['analysis']['coverage_percentage'] for r in session_results)
                    total_completeness = sum(r['analysis']['completeness'] for r in session_results)
                    avg_coverage = total_coverage / len(session_results)
                    avg_completeness = total_completeness / len(session_results)
                    
                    print(f"翻译次数: {len(session_results)}")
                    print(f"平均覆盖率: {avg_coverage:.2f}%")
                    print(f"平均完整度: {avg_completeness:.2f}%")
                    print()
                    
                    print("最近5次翻译:")
                    for i, result in enumerate(session_results[-5:], 1):
                        print(f"{i}. {result['original'][:50]}...")
                        print(f"   {result['translated']}")
                        print(f"   覆盖率: {result['analysis']['coverage_percentage']}%")
                        print()
                else:
                    print("本次会话还没有翻译记录。")
                continue
            elif not user_input:
                print("请输入有效的文本。")
                continue
            
            # 执行翻译
            print("\n--- 翻译结果 ---")
            print(f"原文: {user_input}")
            
            # 判断是否为长文本
            if len(user_input) > 100 or '\n' in user_input:
                translated = translator.translate_document(user_input)
            else:
                translated = translator.translate_text(user_input)
            
            print(f"译文: {translated}")
            
            # 分析翻译质量
            analysis = translator.analyze_translation_quality(user_input, translated)
            print(f"\n--- 翻译分析 ---")
            print(f"词汇覆盖率: {analysis['coverage_percentage']}%")
            print(f"翻译完整度: {analysis['completeness']}%")
            print(f"中文比例: {analysis['chinese_ratio']}%")
            
            if analysis['remaining_english_words'] > 0:
                print(f"剩余英文单词: {analysis['remaining_english_words']} 个")
            
            # 保存结果
            session_results.append({
                'original': user_input,
                'translated': translated,
                'analysis': analysis
            })
            
            print("=" * 50)
            
        except KeyboardInterrupt:
            print("\n程序被用户中断。")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            continue
    
    # 保存会话结果
    if session_results:
        session_report = {
            'session_date': '2025-06-17',
            'translator_version': 'final_translator_v3.0',
            'session_statistics': {
                'total_translations': len(session_results),
                'average_coverage': sum(r['analysis']['coverage_percentage'] for r in session_results) / len(session_results),
                'average_completeness': sum(r['analysis']['completeness'] for r in session_results) / len(session_results)
            },
            'translation_history': session_results
        }
        
        with open('interactive_session_report.json', 'w', encoding='utf-8') as f:
            json.dump(session_report, f, ensure_ascii=False, indent=2)
        
        print(f"\n会话记录已保存到 interactive_session_report.json")
        print(f"本次会话共翻译 {len(session_results)} 次")

def batch_test():
    """批量测试功能"""
    translator = FinalTranslator()
    
    # 更多测试用例
    test_cases = [
        # 简单句子
        "Garchomp is a powerful Dragon-type Pokemon.",
        "Heatran resists many common attacks.",
        "Clefable has excellent bulk and utility.",
        
        # 复杂句子
        "This offensive Garchomp set is designed to sweep teams after a Swords Dance boost.",
        "Heatran with Choice Specs can OHKO most Pokemon with Fire Blast or Earth Power.",
        "Clefable with Magic Guard ability can be used as a reliable special wall and cleric.",
        
        # 战斗描述
        "Weavile can revenge kill weakened Dragon-types with Ice Punch priority.",
        "Landorus provides Stealth Rock support and can pivot with U-turn.",
        "Scizor with Choice Band can clean up late game with Bullet Punch.",
        
        # 队伍分析
        "This team core focuses on offensive pressure with multiple setup sweepers.",
        "The defensive backbone consists of Clefable and Heatran for type synergy.",
        "Stealth Rock support from Landorus helps secure important KOs for the team."
    ]
    
    print("=== 批量翻译测试 ===")
    print(f"测试用例数: {len(test_cases)}")
    print()
    
    results = []
    
    for i, text in enumerate(test_cases, 1):
        print(f"--- 测试 {i}/{len(test_cases)} ---")
        print(f"原文: {text}")
        
        translated = translator.translate_text(text)
        print(f"译文: {translated}")
        
        analysis = translator.analyze_translation_quality(text, translated)
        print(f"覆盖率: {analysis['coverage_percentage']}% | 完整度: {analysis['completeness']}%")
        
        results.append({
            'test_id': i,
            'original': text,
            'translated': translated,
            'analysis': analysis
        })
        
        print()
    
    # 统计结果
    avg_coverage = sum(r['analysis']['coverage_percentage'] for r in results) / len(results)
    avg_completeness = sum(r['analysis']['completeness'] for r in results) / len(results)
    avg_chinese_ratio = sum(r['analysis']['chinese_ratio'] for r in results) / len(results)
    
    print("=== 批量测试统计 ===")
    print(f"平均覆盖率: {avg_coverage:.2f}%")
    print(f"平均完整度: {avg_completeness:.2f}%")
    print(f"平均中文比例: {avg_chinese_ratio:.2f}%")
    
    # 保存批量测试结果
    batch_report = {
        'test_date': '2025-06-17',
        'test_type': 'batch_translation_test',
        'translator_version': 'final_translator_v3.0',
        'test_statistics': {
            'total_test_cases': len(results),
            'average_coverage': round(avg_coverage, 2),
            'average_completeness': round(avg_completeness, 2),
            'average_chinese_ratio': round(avg_chinese_ratio, 2)
        },
        'test_results': results
    }
    
    with open('batch_translation_test.json', 'w', encoding='utf-8') as f:
        json.dump(batch_report, f, ensure_ascii=False, indent=2)
    
    print("批量测试报告已保存到 batch_translation_test.json")

def main():
    """主函数"""
    print("选择运行模式:")
    print("1. 交互式翻译演示")
    print("2. 批量测试")
    print("3. 两者都运行")
    
    try:
        choice = input("请选择 (1/2/3): ").strip()
        
        if choice == '1':
            interactive_demo()
        elif choice == '2':
            batch_test()
        elif choice == '3':
            print("首先运行批量测试...")
            batch_test()
            print("\n" + "="*50)
            print("现在开始交互式演示...")
            interactive_demo()
        else:
            print("无效选择，默认运行交互式演示")
            interactive_demo()
    except KeyboardInterrupt:
        print("\n程序被用户中断。")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()