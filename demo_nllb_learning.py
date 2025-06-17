#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NLLB学习模块演示脚本
展示如何使用NLLB-200模型进行多语言翻译学习
"""

import os
import json
from datetime import datetime
from nllb_learning_module import NLLBLearningModule, NLLBTranslationExample, NLLB_LANGUAGE_CODES

def create_demo_data():
    """创建演示数据"""
    demo_data = [
        {
            "source": "Hello, welcome to the Pokemon world!",
            "target": "你好，欢迎来到宝可梦世界！",
            "source_lang": "english",
            "target_lang": "chinese",
            "domain": "pokemon"
        },
        {
            "source": "Pikachu is an Electric-type Pokemon.",
            "target": "皮卡丘是电属性宝可梦。",
            "source_lang": "english",
            "target_lang": "chinese",
            "domain": "pokemon"
        },
        {
            "source": "This strategy is very effective in competitive battles.",
            "target": "这个策略在竞技对战中非常有效。",
            "source_lang": "english",
            "target_lang": "chinese",
            "domain": "gaming"
        },
        {
            "source": "The weather is nice today.",
            "target": "今天天气很好。",
            "source_lang": "english",
            "target_lang": "chinese",
            "domain": "general"
        },
        {
            "source": "Machine learning is fascinating.",
            "target": "机器学习很有趣。",
            "source_lang": "english",
            "target_lang": "chinese",
            "domain": "technology"
        }
    ]
    
    # 保存演示数据
    demo_dir = "demo_nllb_data"
    os.makedirs(demo_dir, exist_ok=True)
    
    with open(os.path.join(demo_dir, "demo_translations.json"), 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, ensure_ascii=False, indent=2)
    
    print(f"演示数据已创建在 {demo_dir} 目录")
    return demo_dir

def demo_basic_usage():
    """演示基本使用方法"""
    print("\n" + "=" * 60)
    print("NLLB学习模块基本使用演示")
    print("=" * 60)
    
    # 创建学习模块
    nllb_module = NLLBLearningModule("nllb_config.json")
    
    # 初始化模型
    print("\n1. 初始化NLLB模型...")
    nllb_module.initialize_model(source_lang="english", target_lang="chinese")
    
    # 测试基本翻译
    print("\n2. 测试基本翻译功能...")
    test_texts = [
        "Hello world!",
        "How are you today?",
        "This is a test sentence."
    ]
    
    for text in test_texts:
        try:
            translation = nllb_module.translate_text(text, "english", "chinese")
            print(f"原文: {text}")
            print(f"译文: {translation}")
            print("-" * 40)
        except Exception as e:
            print(f"翻译失败: {e}")
    
    return nllb_module

def demo_multi_language_translation(nllb_module):
    """演示多语言翻译"""
    print("\n" + "=" * 60)
    print("多语言翻译演示")
    print("=" * 60)
    
    # 测试文本
    test_text = "Hello, this is a beautiful day!"
    
    # 支持的目标语言
    target_languages = ["chinese", "japanese", "korean", "french", "german", "spanish"]
    
    print(f"\n原文 (English): {test_text}")
    print("\n翻译结果:")
    
    for target_lang in target_languages:
        try:
            translation = nllb_module.translate_text(test_text, "english", target_lang)
            lang_code = NLLB_LANGUAGE_CODES[target_lang]
            print(f"{target_lang.capitalize()} ({lang_code}): {translation}")
        except Exception as e:
            print(f"{target_lang.capitalize()}: 翻译失败 - {e}")

def demo_data_loading_and_learning(nllb_module):
    """演示数据加载和学习"""
    print("\n" + "=" * 60)
    print("数据加载和学习演示")
    print("=" * 60)
    
    # 创建演示数据
    demo_dir = create_demo_data()
    
    # 加载数据
    print("\n1. 加载翻译数据...")
    examples = nllb_module.load_translation_data(demo_dir)
    
    if examples:
        print(f"成功加载 {len(examples)} 个翻译样本")
        
        # 显示学习统计
        print("\n2. 学习统计信息:")
        stats = nllb_module.learning_stats
        print(f"总样本数: {stats['total_examples']}")
        print(f"领域分布: {dict(stats['domains'])}")
        print(f"语言对分布: {dict(stats['languages'])}")
        print(f"难度分布: {dict(stats['difficulty_distribution'])}")
        print(f"质量分布: {dict(stats['quality_distribution'])}")
        
        # 显示样本示例
        print("\n3. 样本示例:")
        for i, example in enumerate(examples[:3]):
            print(f"\n样本 {i+1}:")
            print(f"  源文本: {example.source_text}")
            print(f"  目标文本: {example.target_text}")
            print(f"  语言对: {example.source_lang} -> {example.target_lang}")
            print(f"  领域: {example.domain}")
            print(f"  难度: {example.difficulty:.2f}")
            print(f"  质量: {example.quality_score:.2f}")
    else:
        print("未找到有效的翻译数据")

def demo_model_evaluation(nllb_module):
    """演示模型评估"""
    print("\n" + "=" * 60)
    print("模型评估演示")
    print("=" * 60)
    
    if not nllb_module.test_data:
        print("没有测试数据，跳过评估")
        return
    
    print("\n开始评估模型性能...")
    results = nllb_module.evaluate_model()
    
    print(f"\n评估结果:")
    print(f"BLEU分数: {results.get('bleu_score', 0):.2f}")
    print(f"测试样本总数: {results.get('total_samples', 0)}")
    print(f"成功评估样本数: {results.get('evaluated_samples', 0)}")
    print(f"成功率: {results.get('success_rate', 0):.2%}")
    
    # 显示样本翻译
    sample_translations = results.get('sample_translations', [])
    if sample_translations:
        print("\n样本翻译示例:")
        for i, sample in enumerate(sample_translations):
            print(f"\n示例 {i+1}:")
            print(f"  原文: {sample['source']}")
            print(f"  参考译文: {sample['reference']}")
            print(f"  模型译文: {sample['prediction']}")

def demo_advanced_features(nllb_module):
    """演示高级功能"""
    print("\n" + "=" * 60)
    print("高级功能演示")
    print("=" * 60)
    
    # 1. 语言检测
    print("\n1. 自动语言检测:")
    test_texts = [
        "Hello world",
        "你好世界",
        "こんにちは世界",
        "안녕하세요 세계",
        "Bonjour le monde"
    ]
    
    for text in test_texts:
        detected_lang = nllb_module._detect_language(text)
        print(f"  '{text}' -> {detected_lang}")
    
    # 2. 领域分类
    print("\n2. 领域分类:")
    domain_texts = [
        "Pikachu is a powerful Electric-type Pokemon",
        "This game strategy is very effective",
        "The weather is nice today",
        "Machine learning algorithms are complex"
    ]
    
    for text in domain_texts:
        domain = nllb_module._classify_domain(text)
        print(f"  '{text}' -> {domain}")
    
    # 3. 难度评估
    print("\n3. 翻译难度评估:")
    difficulty_texts = [
        ("Hi", "你好"),
        ("How are you?", "你好吗？"),
        ("This is a complex sentence with technical terminology", "这是一个包含技术术语的复杂句子")
    ]
    
    for source, target in difficulty_texts:
        difficulty = nllb_module._assess_difficulty(source, target)
        print(f"  '{source}' -> 难度: {difficulty:.2f}")

def demo_batch_translation(nllb_module):
    """演示批量翻译"""
    print("\n" + "=" * 60)
    print("批量翻译演示")
    print("=" * 60)
    
    # 批量翻译文本
    batch_texts = [
        "Good morning!",
        "How can I help you?",
        "Thank you very much.",
        "See you later.",
        "Have a nice day!"
    ]
    
    print("\n英文 -> 中文批量翻译:")
    for i, text in enumerate(batch_texts, 1):
        try:
            translation = nllb_module.translate_text(text, "english", "chinese")
            print(f"{i}. {text} -> {translation}")
        except Exception as e:
            print(f"{i}. {text} -> 翻译失败: {e}")
    
    # 测试其他语言对
    print("\n中文 -> 英文翻译:")
    chinese_texts = ["你好", "谢谢", "再见", "祝你好运"]
    
    for i, text in enumerate(chinese_texts, 1):
        try:
            translation = nllb_module.translate_text(text, "chinese", "english")
            print(f"{i}. {text} -> {translation}")
        except Exception as e:
            print(f"{i}. {text} -> 翻译失败: {e}")

def demo_save_report(nllb_module):
    """演示保存学习报告"""
    print("\n" + "=" * 60)
    print("保存学习报告演示")
    print("=" * 60)
    
    print("\n生成并保存学习报告...")
    report_path = nllb_module.save_learning_report()
    
    print(f"报告已保存至: {report_path}")
    
    # 读取并显示报告摘要
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        print("\n报告摘要:")
        print(f"生成时间: {report['timestamp']}")
        print(f"模型: {report['model_config']['model_name']}")
        print(f"支持语言数: {len(report['supported_languages'])}")
        
        data_summary = report['data_summary']
        print(f"数据统计:")
        print(f"  总样本数: {data_summary['total_examples']}")
        print(f"  训练样本: {data_summary['training_examples']}")
        print(f"  验证样本: {data_summary['validation_examples']}")
        print(f"  测试样本: {data_summary['test_examples']}")
        
        if 'evaluation_results' in report and report['evaluation_results']:
            eval_results = report['evaluation_results']
            print(f"评估结果:")
            print(f"  BLEU分数: {eval_results.get('bleu_score', 0):.2f}")
            print(f"  成功率: {eval_results.get('success_rate', 0):.2%}")
    
    except Exception as e:
        print(f"读取报告失败: {e}")

def main():
    """主演示函数"""
    print("NLLB学习模块完整演示")
    print("=" * 80)
    
    try:
        # 基本使用演示
        nllb_module = demo_basic_usage()
        
        # 多语言翻译演示
        demo_multi_language_translation(nllb_module)
        
        # 数据加载和学习演示
        demo_data_loading_and_learning(nllb_module)
        
        # 模型评估演示
        demo_model_evaluation(nllb_module)
        
        # 高级功能演示
        demo_advanced_features(nllb_module)
        
        # 批量翻译演示
        demo_batch_translation(nllb_module)
        
        # 保存报告演示
        demo_save_report(nllb_module)
        
        print("\n" + "=" * 80)
        print("演示完成！")
        print("=" * 80)
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()