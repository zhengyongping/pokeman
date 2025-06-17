#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的NLLB测试脚本
用于验证NLLB学习模块的基本功能
"""

import sys
import os
import json
from datetime import datetime

def test_basic_functionality():
    """测试基本功能"""
    print("=" * 60)
    print("NLLB学习模块基本功能测试")
    print("=" * 60)
    
    try:
        # 导入模块
        print("1. 导入NLLB学习模块...")
        from nllb_learning_module import NLLBLearningModule
        print("   ✓ 模块导入成功")
        
        # 创建模块实例
        print("\n2. 创建模块实例...")
        nllb_module = NLLBLearningModule("nllb_config.json")
        print(f"   ✓ 模块实例创建成功")
        print(f"   设备: {nllb_module.device}")
        
        # 加载数据
        print("\n3. 加载翻译数据...")
        examples = nllb_module.load_translation_data("individual_pairs")
        print(f"   ✓ 成功加载 {len(examples)} 个翻译样本")
        
        if examples:
            print(f"   训练集: {len(nllb_module.training_data)} 样本")
            print(f"   验证集: {len(nllb_module.validation_data)} 样本")
            print(f"   测试集: {len(nllb_module.test_data)} 样本")
            
            # 显示第一个样本
            first_example = examples[0]
            print(f"\n   示例样本:")
            print(f"   源文本: {first_example.source_text[:100]}...")
            print(f"   目标文本: {first_example.target_text[:100]}...")
            print(f"   源语言: {first_example.source_lang}")
            print(f"   目标语言: {first_example.target_lang}")
            print(f"   领域: {first_example.domain}")
            print(f"   难度: {first_example.difficulty:.2f}")
            print(f"   质量: {first_example.quality_score:.2f}")
        
        # 测试语言检测
        print("\n4. 测试语言检测...")
        test_texts = [
            "Hello world",
            "你好世界",
            "こんにちは世界",
            "안녕하세요 세계"
        ]
        
        for text in test_texts:
            detected_lang = nllb_module._detect_language(text)
            print(f"   '{text}' -> {detected_lang}")
        
        # 测试领域分类
        print("\n5. 测试领域分类...")
        test_domains = [
            "This is a Pokemon battle strategy",
            "Let's play this game together",
            "Hello, how are you today?"
        ]
        
        for text in test_domains:
            domain = nllb_module._classify_domain(text)
            print(f"   '{text}' -> {domain}")
        
        # 显示学习统计
        print("\n6. 学习统计信息:")
        stats = nllb_module.learning_stats
        print(f"   总样本数: {stats['total_examples']}")
        print(f"   领域分布: {dict(stats['domains'])}")
        print(f"   语言对: {dict(stats['languages'])}")
        print(f"   难度分布: {dict(stats['difficulty_distribution'])}")
        print(f"   质量分布: {dict(stats['quality_distribution'])}")
        
        print("\n" + "=" * 60)
        print("✅ 所有基本功能测试通过！")
        print("=" * 60)
        
        return True, nllb_module
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_model_initialization(nllb_module):
    """测试模型初始化"""
    print("\n" + "=" * 60)
    print("NLLB模型初始化测试")
    print("=" * 60)
    
    try:
        print("1. 初始化NLLB模型...")
        nllb_module.initialize_model("english", "chinese")
        print("   ✓ 模型初始化成功")
        
        print("\n2. 测试简单翻译...")
        test_text = "Hello, how are you?"
        print(f"   原文: {test_text}")
        
        translated = nllb_module.translate_text(test_text, "english", "chinese")
        print(f"   译文: {translated}")
        
        print("\n✅ 模型初始化和翻译测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print(f"测试开始时间: {datetime.now()}")
    
    # 基本功能测试
    success, nllb_module = test_basic_functionality()
    if not success:
        print("\n基本功能测试失败，退出")
        return False
    
    # 模型初始化测试（可选，因为需要下载模型）
    print("\n是否进行模型初始化测试？(需要下载模型，可能较慢)")
    print("输入 'y' 继续，其他键跳过...")
    
    try:
        # 在自动化环境中跳过交互
        user_input = input().strip().lower()
        if user_input == 'y':
            model_success = test_model_initialization(nllb_module)
            if not model_success:
                print("\n模型测试失败，但基本功能正常")
        else:
            print("\n跳过模型初始化测试")
    except (EOFError, KeyboardInterrupt):
        print("\n跳过模型初始化测试")
    
    print("\n" + "=" * 60)
    print("🎉 NLLB学习系统测试完成！")
    print("=" * 60)
    
    print("\n下一步操作建议:")
    print("1. 运行完整学习程序: python run_nllb_learning.py")
    print("2. 运行演示程序: python demo_nllb_learning.py")
    print("3. 查看配置文件: nllb_config.json")
    print("4. 查看数据目录: individual_pairs/")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n用户中断测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n测试过程中发生未预期错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)