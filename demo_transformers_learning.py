#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transformers学习模块演示脚本
展示如何使用Hugging Face Transformers进行翻译学习
"""

import os
import sys
import json
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from transformers_learning_module import TransformersLearningModule, TranslationExample
    TRANSFORMERS_AVAILABLE = True
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所需依赖: pip install transformers torch numpy")
    TRANSFORMERS_AVAILABLE = False

def demo_basic_usage():
    """基础使用演示"""
    print("=" * 60)
    print("Transformers学习模块 - 基础使用演示")
    print("=" * 60)
    
    if not TRANSFORMERS_AVAILABLE:
        print("Transformers库不可用，跳过演示")
        return
    
    try:
        # 1. 创建学习模块（使用小型模型进行演示）
        print("\n1. 初始化学习模块...")
        learning_module = TransformersLearningModule(
            model_name="google/mt5-small",  # 小型模型，适合演示
            device="auto"
        )
        
        # 2. 加载翻译对数据
        print("\n2. 加载翻译对数据...")
        learning_module.load_translation_pairs("individual_pairs")
        
        if not learning_module.training_examples:
            print("没有找到训练数据，创建示例数据进行演示...")
            create_demo_data(learning_module)
        
        # 3. 显示数据统计
        print("\n3. 数据统计:")
        print(f"   训练样本: {len(learning_module.training_examples)}")
        print(f"   验证样本: {len(learning_module.validation_examples)}")
        print(f"   宝可梦术语: {len(learning_module.pokemon_terms)}")
        print(f"   招式术语: {len(learning_module.move_terms)}")
        
        # 4. 测试基础翻译（使用预训练模型）
        print("\n4. 测试基础翻译（预训练模型）:")
        test_texts = [
            "Giratina-O is a powerful Ghost/Dragon-type Pokemon.",
            "This Pokemon can learn Shadow Ball and Dragon Pulse.",
            "It has excellent offensive capabilities in battle."
        ]
        
        for text in test_texts:
            try:
                translation = learning_module.translate_text(text)
                print(f"   原文: {text}")
                print(f"   译文: {translation}")
                print()
            except Exception as e:
                print(f"   翻译失败: {e}")
        
        # 5. 微调模型（如果有足够的数据）
        if len(learning_module.training_examples) >= 5:
            print("\n5. 开始微调模型...")
            print("   注意: 这可能需要几分钟时间")
            
            try:
                learning_module.fine_tune_model(
                    output_dir="./demo_fine_tuned_model",
                    num_epochs=1,  # 演示用，只训练1个epoch
                    batch_size=2,  # 小批次大小
                    learning_rate=5e-5,
                    save_steps=100,
                    eval_steps=50
                )
                
                print("   微调完成！")
                
                # 6. 测试微调后的翻译
                print("\n6. 测试微调后的翻译:")
                for text in test_texts:
                    try:
                        translation = learning_module.translate_text(text)
                        print(f"   原文: {text}")
                        print(f"   译文: {translation}")
                        print()
                    except Exception as e:
                        print(f"   翻译失败: {e}")
                
                # 7. 评估模型
                print("\n7. 评估模型性能:")
                evaluation_results = learning_module.evaluate_model()
                for metric, value in evaluation_results.items():
                    print(f"   {metric}: {value:.3f}")
                
            except Exception as e:
                print(f"   微调过程出错: {e}")
                print("   这可能是由于内存不足或其他系统限制")
        
        else:
            print("\n5. 跳过微调（训练数据不足）")
        
        # 8. 保存学习报告
        print("\n8. 保存学习报告...")
        report_path = learning_module.save_learning_report()
        print(f"   报告已保存到: {report_path}")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

def create_demo_data(learning_module):
    """创建演示数据"""
    demo_examples = [
        TranslationExample(
            source_text="Giratina-O is a powerful Ghost/Dragon-type Pokemon with excellent offensive capabilities.",
            target_text="骑拉帝纳-起源形态是一只强大的幽灵/龙属性宝可梦，具有出色的攻击能力。",
            domain="pokemon",
            difficulty=0.7,
            quality_score=0.9
        ),
        TranslationExample(
            source_text="Shadow Ball is a special Ghost-type move that can lower the target's Special Defense.",
            target_text="影子球是一个特殊的幽灵属性招式，可以降低目标的特殊防御。",
            domain="pokemon",
            difficulty=0.6,
            quality_score=0.8
        ),
        TranslationExample(
            source_text="This Pokemon can check many threats in the current metagame.",
            target_text="这只宝可梦可以制衡当前环境中的许多威胁。",
            domain="strategy",
            difficulty=0.8,
            quality_score=0.9
        ),
        TranslationExample(
            source_text="Dragon Dance boosts both Attack and Speed stats.",
            target_text="龙之舞可以同时提升攻击和速度数值。",
            domain="pokemon",
            difficulty=0.5,
            quality_score=0.9
        ),
        TranslationExample(
            source_text="Stealth Rock is an entry hazard that damages Pokemon switching in.",
            target_text="隐形岩是一种入场危险，会对切换进场的宝可梦造成伤害。",
            domain="pokemon",
            difficulty=0.7,
            quality_score=0.8
        ),
        TranslationExample(
            source_text="This set provides excellent coverage against common threats.",
            target_text="这个配置对常见威胁提供了出色的打击面。",
            domain="strategy",
            difficulty=0.6,
            quality_score=0.8
        )
    ]
    
    # 分配到训练集和验证集
    for i, example in enumerate(demo_examples):
        if i < 4:  # 前4个作为训练集
            learning_module.training_examples.append(example)
        else:  # 后2个作为验证集
            learning_module.validation_examples.append(example)
    
    # 更新统计信息
    learning_module.learning_stats["total_examples"] = len(demo_examples)
    learning_module.learning_stats["training_examples"] = len(learning_module.training_examples)
    learning_module.learning_stats["validation_examples"] = len(learning_module.validation_examples)
    
    # 添加一些术语
    learning_module.pokemon_terms.update({
        "Giratina-O": "骑拉帝纳-起源",
        "Pokemon": "宝可梦",
        "Ghost": "幽灵",
        "Dragon": "龙"
    })
    
    learning_module.move_terms.update({
        "Shadow Ball": "影子球",
        "Dragon Dance": "龙之舞",
        "Stealth Rock": "隐形岩"
    })
    
    print("   已创建演示数据")

def demo_model_comparison():
    """模型对比演示"""
    print("\n" + "=" * 60)
    print("模型对比演示")
    print("=" * 60)
    
    if not TRANSFORMERS_AVAILABLE:
        print("Transformers库不可用，跳过演示")
        return
    
    models_to_test = [
        "google/mt5-small",
        # "facebook/mbart-large-50-many-to-many-mmt",  # 较大的模型，可能需要更多内存
        # "Helsinki-NLP/opus-mt-en-zh"  # 专门的英中翻译模型
    ]
    
    test_text = "Giratina-O is a powerful Ghost/Dragon-type Pokemon."
    
    for model_name in models_to_test:
        try:
            print(f"\n测试模型: {model_name}")
            learning_module = TransformersLearningModule(model_name=model_name)
            
            translation = learning_module.translate_text(test_text)
            print(f"原文: {test_text}")
            print(f"译文: {translation}")
            
        except Exception as e:
            print(f"模型 {model_name} 测试失败: {e}")

def demo_advanced_features():
    """高级功能演示"""
    print("\n" + "=" * 60)
    print("高级功能演示")
    print("=" * 60)
    
    if not TRANSFORMERS_AVAILABLE:
        print("Transformers库不可用，跳过演示")
        return
    
    try:
        learning_module = TransformersLearningModule()
        
        # 1. 术语提取演示
        print("\n1. 术语提取演示:")
        sample_text = "Mega Garchomp can use Dragon Dance to boost its Attack and Speed stats."
        sample_chinese = "超级烈咬陆鲨可以使用龙之舞来提升它的攻击和速度数值。"
        
        learning_module._extract_terms(sample_text, sample_chinese)
        print(f"   提取的宝可梦术语: {learning_module.pokemon_terms}")
        print(f"   提取的招式术语: {learning_module.move_terms}")
        
        # 2. 文本分类演示
        print("\n2. 文本分类演示:")
        test_texts = [
            "Giratina-O is a Ghost/Dragon-type Pokemon.",
            "This strategy works well in the current metagame.",
            "The weather is nice today."
        ]
        
        for text in test_texts:
            domain = learning_module._classify_domain(text)
            difficulty = learning_module._assess_difficulty(text)
            print(f"   文本: {text}")
            print(f"   领域: {domain}, 难度: {difficulty:.2f}")
        
        # 3. 质量评估演示
        print("\n3. 翻译质量评估演示:")
        quality_examples = [
            ("Hello", "你好"),
            ("This is a test", "这是一个测试"),
            ("Very long English sentence", "短中文")
        ]
        
        for en, cn in quality_examples:
            quality = learning_module._assess_quality(en, cn)
            print(f"   英文: {en} -> 中文: {cn}")
            print(f"   质量评分: {quality:.2f}")
        
    except Exception as e:
        print(f"高级功能演示出错: {e}")

def main():
    """主函数"""
    print("Transformers学习模块演示程序")
    print("作者: AI Assistant")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查依赖
    if not TRANSFORMERS_AVAILABLE:
        print("\n错误: 缺少必要的依赖库")
        print("请运行以下命令安装:")
        print("pip install transformers torch numpy scipy sacrebleu")
        return
    
    try:
        # 基础使用演示
        demo_basic_usage()
        
        # 模型对比演示
        demo_model_comparison()
        
        # 高级功能演示
        demo_advanced_features()
        
        print("\n" + "=" * 60)
        print("演示完成！")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n演示被用户中断")
    except Exception as e:
        print(f"\n演示过程中出现未预期的错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()