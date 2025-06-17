# -*- coding: utf-8 -*-
"""
测试高级文本翻译器
"""

import json
from advanced_text_translator import AdvancedTextTranslator

def test_translator():
    """测试翻译器功能"""
    print("=== 测试高级文本翻译器 ===")
    
    # 创建翻译器实例
    translator = AdvancedTextTranslator()
    print(f"已加载词典: {len(translator.dictionary)} 个术语")
    print(f"短语模式: {len(translator.phrase_patterns)} 个")
    print(f"句子模板: {len(translator.sentence_templates)} 个")
    print()
    
    # 测试用例
    test_cases = [
        {
            'name': '简单句子翻译',
            'text': 'Garchomp is a great sweeper with Swords Dance.'
        },
        {
            'name': '复杂句子翻译',
            'text': 'This Heatran set is designed to provide special attack coverage with Choice Specs.'
        },
        {
            'name': '战斗描述翻译',
            'text': 'Weavile can OHKO Garchomp with Ice Punch after Stealth Rock damage.'
        },
        {
            'name': '配置描述翻译',
            'text': 'Clefable with Magic Guard ability can be used as a special wall.'
        },
        {
            'name': '长文本翻译',
            'text': '''This team focuses on offensive pressure. Garchomp serves as the primary physical sweeper with Swords Dance setup. Heatran provides special attack coverage and Stealth Rock support. Clefable acts as a reliable special wall with Magic Guard ability.'''
        }
    ]
    
    results = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"--- 测试 {i}: {case['name']} ---")
        print(f"原文: {case['text']}")
        
        # 执行翻译
        if '\n' in case['text'] or len(case['text']) > 100:
            translated = translator.translate_document(case['text'])
        else:
            translated = translator.translate_text(case['text'])
        
        print(f"译文: {translated}")
        
        # 分析覆盖率
        analysis = translator.analyze_translation_coverage(case['text'])
        print(f"覆盖率: {analysis['coverage_percentage']}% ({analysis['translated_words']}/{analysis['total_words']})")
        
        if analysis['untranslated_words']:
            print(f"未翻译: {', '.join(analysis['untranslated_words'][:5])}")
        
        results.append({
            'test_name': case['name'],
            'original': case['text'],
            'translated': translated,
            'coverage': analysis['coverage_percentage'],
            'translated_words': analysis['translated_words'],
            'total_words': analysis['total_words']
        })
        
        print("=" * 60)
        print()
    
    # 计算总体统计
    total_words = sum(r['total_words'] for r in results)
    total_translated = sum(r['translated_words'] for r in results)
    overall_coverage = (total_translated / total_words * 100) if total_words > 0 else 0
    
    print("=== 总体统计 ===")
    print(f"测试用例数: {len(results)}")
    print(f"总词数: {total_words}")
    print(f"已翻译词数: {total_translated}")
    print(f"总体覆盖率: {overall_coverage:.2f}%")
    print()
    
    # 保存测试结果
    test_report = {
        'test_date': '2025-06-17',
        'translator_version': 'advanced_text_translator_v1.0',
        'test_results': results,
        'overall_statistics': {
            'total_test_cases': len(results),
            'total_words': total_words,
            'total_translated_words': total_translated,
            'overall_coverage_percentage': round(overall_coverage, 2)
        },
        'translator_capabilities': {
            'dictionary_size': len(translator.dictionary),
            'phrase_patterns': len(translator.phrase_patterns),
            'sentence_templates': len(translator.sentence_templates)
        }
    }
    
    with open('translation_test_report.json', 'w', encoding='utf-8') as f:
        json.dump(test_report, f, ensure_ascii=False, indent=2)
    
    print("测试报告已保存到 translation_test_report.json")
    
    return test_report

if __name__ == "__main__":
    test_translator()