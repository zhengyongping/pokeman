#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版Transformers学习模块演示脚本
展示如何使用新的增强版学习模块进行翻译学习和评估
"""

import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any

try:
    from enhanced_transformers_module import (
        EnhancedTransformersModule, 
        EnhancedTranslationExample,
        ModelConfig,
        TrainingConfig
    )
    MODULE_AVAILABLE = True
except ImportError as e:
    print(f"导入模块失败: {e}")
    MODULE_AVAILABLE = False

def create_demo_data(output_dir: str = "demo_pairs") -> int:
    """
    创建演示用的翻译对数据
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    demo_pairs = [
        {
            "english": "Giratina-O is a powerful Ghost/Dragon-type Pokemon with excellent offensive capabilities.",
            "chinese": "骑拉帝纳-起源形态是一只强大的幽灵/龙属性宝可梦，具有出色的攻击能力。"
        },
        {
            "english": "Mega Garchomp has increased Attack and Special Attack stats but reduced Speed.",
            "chinese": "超级烈咬陆鲨的攻击力和特攻有所提升，但速度降低了。"
        },
        {
            "english": "Shadow Ball is a Ghost-type special move that may lower the target's Special Defense.",
            "chinese": "暗影球是幽灵属性的特殊招式，可能会降低目标的特防。"
        },
        {
            "english": "The Choice Band increases Attack by 50% but locks the user into the first move used.",
            "chinese": "讲究头带能提升50%的攻击力，但会锁定使用者只能使用第一个招式。"
        },
        {
            "english": "Stealth Rock is an entry hazard that damages Pokemon switching in based on their Rock-type weakness.",
            "chinese": "隐形岩是一种入场危险招式，会根据岩石属性克制关系对切换上场的宝可梦造成伤害。"
        },
        {
            "english": "Thunder Wave paralyzes the target and reduces their Speed by 75%.",
            "chinese": "电磁波会让目标陷入麻痹状态，并将其速度降低75%。"
        },
        {
            "english": "Rotom-W is a Water/Electric-type Pokemon that resists many common attacking types.",
            "chinese": "洛托姆-冲洗形态是水/电属性宝可梦，能抵抗许多常见的攻击属性。"
        },
        {
            "english": "The Leftovers item restores 1/16 of the holder's maximum HP at the end of each turn.",
            "chinese": "吃剩的东西道具会在每回合结束时恢复持有者最大HP的1/16。"
        },
        {
            "english": "Earthquake is a powerful Ground-type move that hits all Pokemon on the field except the user.",
            "chinese": "地震是强力的地面属性招式，会攻击场上除使用者外的所有宝可梦。"
        },
        {
            "english": "Toxic Spikes poison Pokemon that switch in, with two layers causing badly poisoned status.",
            "chinese": "毒菱会让切换上场的宝可梦中毒，两层毒菱会造成剧毒状态。"
        },
        {
            "english": "Scizor's Bullet Punch is a priority Steel-type move that always goes first.",
            "chinese": "巨钳螳螂的子弹拳是优先度钢属性招式，总是能够先制攻击。"
        },
        {
            "english": "The Assault Vest boosts Special Defense by 50% but prevents the use of status moves.",
            "chinese": "突击背心能提升50%的特防，但会阻止使用变化招式。"
        },
        {
            "english": "Rapid Spin removes entry hazards from the user's side and deals damage to the target.",
            "chinese": "高速旋转能清除己方场地的入场危险招式，并对目标造成伤害。"
        },
        {
            "english": "Dragonite's Multiscale ability reduces damage by 50% when at full HP.",
            "chinese": "快龙的多重鳞片特性在满血时能减少50%的伤害。"
        },
        {
            "english": "Will-O-Wisp burns the target, reducing their Attack and dealing damage each turn.",
            "chinese": "鬼火会让目标陷入灼伤状态，降低其攻击力并每回合造成伤害。"
        },
        {
            "english": "The Life Orb increases move power by 30% but causes recoil damage to the user.",
            "chinese": "生命宝珠能提升30%的招式威力，但会对使用者造成反作用力伤害。"
        },
        {
            "english": "Substitute creates a decoy that absorbs damage until it's destroyed.",
            "chinese": "替身会创造一个替身，吸收伤害直到被摧毁。"
        },
        {
            "english": "Tyranitar's Sand Stream ability summons a sandstorm when it enters battle.",
            "chinese": "班基拉斯的扬沙特性会在进入战斗时召唤沙暴。"
        },
        {
            "english": "Focus Sash prevents the user from being knocked out in one hit when at full HP.",
            "chinese": "气势头带能防止满血时被一击击倒。"
        },
        {
            "english": "Calm Mind raises the user's Special Attack and Special Defense by one stage each.",
            "chinese": "冥想会将使用者的特攻和特防各提升一个等级。"
        }
    ]
    
    # 保存演示数据
    for i, pair in enumerate(demo_pairs):
        filename = f"demo_pair_{i+1:02d}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(pair, f, ensure_ascii=False, indent=2)
    
    print(f"已创建 {len(demo_pairs)} 个演示翻译对到目录: {output_dir}")
    return len(demo_pairs)

def demonstrate_basic_usage():
    """
    演示基本使用方法
    """
    print("\n=== 基本使用演示 ===")
    
    try:
        # 初始化模块
        print("1. 初始化增强版Transformers学习模块...")
        module = EnhancedTransformersModule(
            config_path="transformers_config.json",
            model_key="mt5_small",
            device="auto"
        )
        
        print(f"   模型: {module.model_config.name}")
        print(f"   设备: {module.device}")
        print(f"   最大长度: {module.model_config.max_length}")
        
        # 创建演示数据
        print("\n2. 创建演示数据...")
        demo_count = create_demo_data()
        
        # 加载数据
        print("\n3. 加载翻译数据...")
        module.load_translation_data(
            pairs_directory="demo_pairs",
            train_ratio=0.7,
            val_ratio=0.2,
            test_ratio=0.1
        )
        
        # 显示数据统计
        print("\n4. 数据统计:")
        print(f"   训练集: {len(module.training_examples)} 个样本")
        print(f"   验证集: {len(module.validation_examples)} 个样本")
        print(f"   测试集: {len(module.test_examples)} 个样本")
        
        # 显示术语统计
        total_terms = sum(len(d) for d in module.term_dictionaries.values())
        print(f"   提取术语: {total_terms} 个")
        
        for term_type, terms in module.term_dictionaries.items():
            if terms:
                print(f"     {term_type}: {len(terms)} 个")
                # 显示前3个术语
                sample_terms = list(terms.items())[:3]
                for en, cn in sample_terms:
                    print(f"       {en} -> {cn}")
        
        # 测试基础翻译
        print("\n5. 测试基础翻译能力...")
        test_texts = [
            "Giratina-O is very powerful.",
            "Mega Garchomp has high Attack.",
            "Shadow Ball is a Ghost-type move."
        ]
        
        for text in test_texts:
            translation = module.translate_text(text)
            print(f"   原文: {text}")
            print(f"   译文: {translation}")
            print()
        
        return module
        
    except Exception as e:
        print(f"基本使用演示失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def demonstrate_fine_tuning(module: EnhancedTransformersModule):
    """
    演示模型微调
    """
    print("\n=== 模型微调演示 ===")
    
    if not module or not module.training_examples:
        print("没有可用的训练数据，跳过微调演示")
        return
    
    try:
        # 使用快速配置进行微调
        print("1. 开始模型微调（使用快速配置）...")
        
        # 自定义快速训练配置
        quick_config = {
            "num_epochs": 2,
            "learning_rate": 5e-5,
            "warmup_steps": 100,
            "save_steps": 500,
            "eval_steps": 250,
            "description": "快速演示配置"
        }
        
        start_time = time.time()
        
        train_result = module.fine_tune_model(
            custom_config=quick_config,
            output_dir="./demo_fine_tuned_model"
        )
        
        end_time = time.time()
        training_time = end_time - start_time
        
        print(f"\n2. 微调完成！")
        print(f"   训练时间: {training_time:.2f} 秒")
        
        if train_result:
            print(f"   最终训练损失: {train_result.training_loss:.4f}")
            if hasattr(train_result, 'eval_loss') and train_result.eval_loss:
                print(f"   最终验证损失: {train_result.eval_loss:.4f}")
        
        # 测试微调后的翻译效果
        print("\n3. 测试微调后的翻译效果...")
        test_texts = [
            "Giratina-O is a powerful Ghost/Dragon-type Pokemon.",
            "Mega Garchomp has increased Attack stats.",
            "Shadow Ball may lower Special Defense."
        ]
        
        for text in test_texts:
            translation = module.translate_text(text, num_beams=4)
            print(f"   原文: {text}")
            print(f"   译文: {translation}")
            print()
        
    except Exception as e:
        print(f"微调演示失败: {e}")
        import traceback
        traceback.print_exc()

def demonstrate_evaluation(module: EnhancedTransformersModule):
    """
    演示模型评估
    """
    print("\n=== 模型评估演示 ===")
    
    if not module:
        print("模块不可用，跳过评估演示")
        return
    
    try:
        # 综合评估
        print("1. 进行综合模型评估...")
        
        evaluation_results = module.comprehensive_evaluate()
        
        if evaluation_results:
            print("\n2. 评估结果:")
            print(f"   语料库BLEU分数: {evaluation_results.get('corpus_bleu', 0):.2f}")
            print(f"   平均句子BLEU分数: {evaluation_results.get('avg_sentence_bleu', 0):.2f}")
            print(f"   平均字符相似度: {evaluation_results.get('avg_character_similarity', 0):.3f}")
            print(f"   平均长度比例: {evaluation_results.get('avg_length_ratio', 0):.3f}")
            print(f"   测试样本数: {evaluation_results.get('total_samples', 0)}")
            
            # 显示按领域的评估结果
            domain_results = {k: v for k, v in evaluation_results.items() if k.endswith('_avg_score')}
            if domain_results:
                print("\n   按领域评估结果:")
                for domain_key, score in domain_results.items():
                    domain_name = domain_key.replace('_avg_score', '')
                    sample_count_key = f"{domain_name}_sample_count"
                    sample_count = evaluation_results.get(sample_count_key, 0)
                    print(f"     {domain_name}: {score:.3f} ({sample_count} 个样本)")
        
        # 单独测试一些样本
        print("\n3. 单独样本测试:")
        if module.test_examples:
            test_samples = module.test_examples[:3]  # 取前3个测试样本
        elif module.validation_examples:
            test_samples = module.validation_examples[:3]
        else:
            test_samples = module.training_examples[:3]
        
        for i, example in enumerate(test_samples, 1):
            predicted = module.translate_text(example.source_text)
            print(f"\n   样本 {i}:")
            print(f"     原文: {example.source_text}")
            print(f"     参考译文: {example.target_text}")
            print(f"     模型译文: {predicted}")
            print(f"     领域: {example.domain}")
            print(f"     难度: {example.difficulty:.2f}")
            print(f"     质量: {example.quality_score:.2f}")
        
    except Exception as e:
        print(f"评估演示失败: {e}")
        import traceback
        traceback.print_exc()

def demonstrate_advanced_features(module: EnhancedTransformersModule):
    """
    演示高级功能
    """
    print("\n=== 高级功能演示 ===")
    
    if not module:
        print("模块不可用，跳过高级功能演示")
        return
    
    try:
        # 1. 术语提取和映射
        print("1. 术语提取和映射功能:")
        total_terms = sum(len(d) for d in module.term_dictionaries.values())
        print(f"   总提取术语数: {total_terms}")
        
        for term_type, terms in module.term_dictionaries.items():
            if terms:
                print(f"   {term_type}: {len(terms)} 个术语")
                # 显示一些示例
                sample_terms = list(terms.items())[:2]
                for en, cn in sample_terms:
                    print(f"     {en} -> {cn}")
        
        # 2. 不同翻译参数测试
        print("\n2. 不同翻译参数测试:")
        test_text = "Giratina-O is a powerful Ghost/Dragon-type Pokemon with excellent offensive capabilities."
        
        # 不同beam数量
        for num_beams in [1, 3, 5]:
            translation = module.translate_text(test_text, num_beams=num_beams)
            print(f"   Beam={num_beams}: {translation}")
        
        # 3. 数据质量分析
        print("\n3. 数据质量分析:")
        all_examples = module.training_examples + module.validation_examples + module.test_examples
        
        if all_examples:
            difficulties = [ex.difficulty for ex in all_examples]
            qualities = [ex.quality_score for ex in all_examples]
            
            print(f"   平均难度: {sum(difficulties)/len(difficulties):.3f}")
            print(f"   平均质量: {sum(qualities)/len(qualities):.3f}")
            
            # 按领域统计
            from collections import Counter
            domain_counts = Counter(ex.domain for ex in all_examples)
            print(f"   领域分布: {dict(domain_counts)}")
        
        # 4. 学习统计信息
        print("\n4. 学习统计信息:")
        stats = module.learning_stats
        print(f"   模型信息: {stats['model_info']['name']}")
        print(f"   训练轮数: {stats.get('epochs_trained', 0)}")
        print(f"   训练时间: {stats.get('training_time', 0):.2f} 秒")
        
        if stats.get('best_scores'):
            print(f"   最佳BLEU分数: {stats['best_scores'].get('corpus_bleu', 0):.2f}")
        
        # 5. 保存综合报告
        print("\n5. 保存综合学习报告...")
        report_path = module.save_comprehensive_report()
        print(f"   报告已保存到: {report_path}")
        
        # 显示报告摘要
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        print("\n   报告摘要:")
        print(f"     生成时间: {report['metadata']['generation_time']}")
        print(f"     总参数量: {report['metadata']['total_parameters']:,}")
        print(f"     数据样本总数: {report['data_statistics']['total_examples']}")
        
    except Exception as e:
        print(f"高级功能演示失败: {e}")
        import traceback
        traceback.print_exc()

def demonstrate_model_comparison():
    """
    演示不同模型的比较
    """
    print("\n=== 模型比较演示 ===")
    
    # 检查配置文件是否存在
    if not os.path.exists("transformers_config.json"):
        print("配置文件不存在，跳过模型比较演示")
        return
    
    try:
        # 加载配置
        with open("transformers_config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        available_models = list(config.get("models", {}).keys())
        print(f"可用模型: {available_models}")
        
        # 选择几个轻量级模型进行比较
        test_models = [model for model in available_models if "small" in model or "base" in model][:2]
        
        if not test_models:
            print("没有找到适合比较的轻量级模型")
            return
        
        test_text = "Giratina-O is powerful."
        results = {}
        
        for model_key in test_models:
            try:
                print(f"\n测试模型: {model_key}")
                
                # 创建模块实例
                module = EnhancedTransformersModule(
                    config_path="transformers_config.json",
                    model_key=model_key
                )
                
                # 测试翻译
                start_time = time.time()
                translation = module.translate_text(test_text)
                end_time = time.time()
                
                results[model_key] = {
                    "translation": translation,
                    "time": end_time - start_time,
                    "model_name": module.model_config.name
                }
                
                print(f"  模型名称: {module.model_config.name}")
                print(f"  翻译结果: {translation}")
                print(f"  翻译时间: {end_time - start_time:.3f} 秒")
                
            except Exception as e:
                print(f"  模型 {model_key} 测试失败: {e}")
                continue
        
        # 比较结果
        if len(results) > 1:
            print("\n模型比较总结:")
            for model_key, result in results.items():
                print(f"  {model_key}:")
                print(f"    翻译: {result['translation']}")
                print(f"    时间: {result['time']:.3f}s")
        
    except Exception as e:
        print(f"模型比较演示失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    """
    主演示函数
    """
    print("增强版Transformers学习模块演示")
    print("=" * 50)
    
    if not MODULE_AVAILABLE:
        print("模块不可用，请检查依赖安装")
        print("运行: pip install transformers torch sacrebleu")
        return
    
    try:
        # 基本使用演示
        module = demonstrate_basic_usage()
        
        if module:
            # 模型微调演示
            demonstrate_fine_tuning(module)
            
            # 模型评估演示
            demonstrate_evaluation(module)
            
            # 高级功能演示
            demonstrate_advanced_features(module)
        
        # 模型比较演示（独立运行）
        demonstrate_model_comparison()
        
        print("\n=== 演示完成 ===")
        print("所有功能演示已完成！")
        print("\n生成的文件:")
        print("  - demo_pairs/: 演示翻译对数据")
        print("  - demo_fine_tuned_model/: 微调后的模型")
        print("  - enhanced_transformers_report_*.json: 学习报告")
        
    except KeyboardInterrupt:
        print("\n演示被用户中断")
    except Exception as e:
        print(f"\n演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()