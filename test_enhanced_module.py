#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版Transformers模块测试脚本
用于验证模块的基本功能和兼容性
"""

import os
import sys
import json
import time
from typing import Dict, Any

def test_imports():
    """
    测试依赖库导入
    """
    print("=== 测试依赖库导入 ===")
    
    try:
        import torch
        print(f"✓ PyTorch版本: {torch.__version__}")
        print(f"  CUDA可用: {torch.cuda.is_available()}")
        if hasattr(torch.backends, 'mps'):
            print(f"  MPS可用: {torch.backends.mps.is_available()}")
    except ImportError:
        print("✗ PyTorch未安装")
        return False
    
    try:
        import transformers
        print(f"✓ Transformers版本: {transformers.__version__}")
    except ImportError:
        print("✗ Transformers未安装")
        return False
    
    try:
        import sacrebleu
        print(f"✓ SacreBLEU版本: {sacrebleu.__version__}")
    except ImportError:
        print("✗ SacreBLEU未安装")
        return False
    
    try:
        import numpy as np
        print(f"✓ NumPy版本: {np.__version__}")
    except ImportError:
        print("✗ NumPy未安装")
        return False
    
    return True

def test_module_import():
    """
    测试模块导入
    """
    print("\n=== 测试模块导入 ===")
    
    try:
        from enhanced_transformers_module import (
            EnhancedTransformersModule,
            EnhancedTranslationExample,
            ModelConfig,
            TrainingConfig,
            EnhancedPokemonDataset
        )
        print("✓ 增强版Transformers模块导入成功")
        return True
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def test_config_file():
    """
    测试配置文件
    """
    print("\n=== 测试配置文件 ===")
    
    config_path = "transformers_config.json"
    
    if not os.path.exists(config_path):
        print(f"✗ 配置文件 {config_path} 不存在")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查必要的配置项
        required_keys = ['models', 'training_configs']
        for key in required_keys:
            if key not in config:
                print(f"✗ 配置文件缺少必要项: {key}")
                return False
        
        print(f"✓ 配置文件格式正确")
        print(f"  可用模型: {list(config['models'].keys())}")
        print(f"  训练配置: {list(config['training_configs'].keys())}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ 配置文件JSON格式错误: {e}")
        return False
    except Exception as e:
        print(f"✗ 配置文件读取失败: {e}")
        return False

def test_module_initialization():
    """
    测试模块初始化
    """
    print("\n=== 测试模块初始化 ===")
    
    try:
        from enhanced_transformers_module import EnhancedTransformersModule
        
        # 测试默认初始化
        print("正在初始化模块...")
        start_time = time.time()
        
        module = EnhancedTransformersModule(
            config_path="transformers_config.json",
            model_key="mt5_small",
            device="auto"
        )
        
        end_time = time.time()
        init_time = end_time - start_time
        
        print(f"✓ 模块初始化成功 (耗时: {init_time:.2f}秒)")
        print(f"  模型: {module.model_config.name}")
        print(f"  设备: {module.device}")
        print(f"  最大长度: {module.model_config.max_length}")
        
        # 检查模型和分词器
        if module.model is None:
            print("✗ 模型未正确加载")
            return False, None
        
        if module.tokenizer is None:
            print("✗ 分词器未正确加载")
            return False, None
        
        # 计算模型参数
        total_params = sum(p.numel() for p in module.model.parameters())
        print(f"  模型参数量: {total_params:,}")
        
        return True, module
        
    except Exception as e:
        print(f"✗ 模块初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_basic_translation(module):
    """
    测试基础翻译功能
    """
    print("\n=== 测试基础翻译功能 ===")
    
    if module is None:
        print("✗ 模块不可用，跳过翻译测试")
        return False
    
    test_texts = [
        "Hello world",
        "Pokemon is great",
        "Pikachu is electric type"
    ]
    
    try:
        for i, text in enumerate(test_texts, 1):
            print(f"\n测试 {i}: {text}")
            
            start_time = time.time()
            translation = module.translate_text(text)
            end_time = time.time()
            
            translate_time = end_time - start_time
            
            print(f"  译文: {translation}")
            print(f"  耗时: {translate_time:.3f}秒")
            
            if not translation or translation.strip() == "":
                print(f"  ⚠️ 翻译结果为空")
            else:
                print(f"  ✓ 翻译成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 翻译测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_structures():
    """
    测试数据结构
    """
    print("\n=== 测试数据结构 ===")
    
    try:
        from enhanced_transformers_module import (
            EnhancedTranslationExample,
            ModelConfig,
            TrainingConfig
        )
        
        # 测试EnhancedTranslationExample
        example = EnhancedTranslationExample(
            source_text="Test English text",
            target_text="测试中文文本",
            domain="test",
            difficulty=0.5,
            quality_score=0.8
        )
        
        print(f"✓ EnhancedTranslationExample创建成功")
        print(f"  原文: {example.source_text}")
        print(f"  译文: {example.target_text}")
        print(f"  领域: {example.domain}")
        print(f"  难度: {example.difficulty}")
        print(f"  质量: {example.quality_score}")
        
        # 测试ModelConfig
        model_config = ModelConfig(
            name="test-model",
            description="测试模型",
            parameters="100M",
            memory_requirement="1GB",
            recommended_batch_size=4,
            max_length=256,
            languages=["en", "zh"],
            use_case="test"
        )
        
        print(f"\n✓ ModelConfig创建成功")
        print(f"  模型名: {model_config.name}")
        print(f"  描述: {model_config.description}")
        
        # 测试TrainingConfig
        training_config = TrainingConfig(
            num_epochs=1,
            learning_rate=1e-5,
            warmup_steps=100,
            save_steps=500,
            eval_steps=250,
            description="测试配置"
        )
        
        print(f"\n✓ TrainingConfig创建成功")
        print(f"  训练轮数: {training_config.num_epochs}")
        print(f"  学习率: {training_config.learning_rate}")
        
        return True
        
    except Exception as e:
        print(f"✗ 数据结构测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_demo_data_creation():
    """
    测试演示数据创建
    """
    print("\n=== 测试演示数据创建 ===")
    
    try:
        from demo_enhanced_transformers import create_demo_data
        
        # 创建测试目录
        test_dir = "test_demo_pairs"
        
        # 创建演示数据
        count = create_demo_data(test_dir)
        
        print(f"✓ 演示数据创建成功")
        print(f"  创建文件数: {count}")
        print(f"  保存目录: {test_dir}")
        
        # 验证文件
        if os.path.exists(test_dir):
            files = [f for f in os.listdir(test_dir) if f.endswith('.json')]
            print(f"  实际文件数: {len(files)}")
            
            # 检查第一个文件
            if files:
                first_file = os.path.join(test_dir, files[0])
                with open(first_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if 'english' in data and 'chinese' in data:
                    print(f"  ✓ 文件格式正确")
                    print(f"    示例英文: {data['english'][:50]}...")
                    print(f"    示例中文: {data['chinese'][:30]}...")
                else:
                    print(f"  ✗ 文件格式错误")
                    return False
        
        return True
        
    except Exception as e:
        print(f"✗ 演示数据创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_loading(module):
    """
    测试数据加载功能
    """
    print("\n=== 测试数据加载功能 ===")
    
    if module is None:
        print("✗ 模块不可用，跳过数据加载测试")
        return False
    
    try:
        # 使用测试数据目录
        test_dir = "test_demo_pairs"
        
        if not os.path.exists(test_dir):
            print(f"✗ 测试数据目录 {test_dir} 不存在")
            return False
        
        # 加载数据
        print("正在加载数据...")
        module.load_translation_data(
            pairs_directory=test_dir,
            train_ratio=0.7,
            val_ratio=0.2,
            test_ratio=0.1
        )
        
        print(f"✓ 数据加载成功")
        print(f"  训练集: {len(module.training_examples)} 个样本")
        print(f"  验证集: {len(module.validation_examples)} 个样本")
        print(f"  测试集: {len(module.test_examples)} 个样本")
        
        # 检查术语提取
        total_terms = sum(len(d) for d in module.term_dictionaries.values())
        print(f"  提取术语: {total_terms} 个")
        
        # 显示一些样本
        if module.training_examples:
            sample = module.training_examples[0]
            print(f"\n  样本示例:")
            print(f"    原文: {sample.source_text[:50]}...")
            print(f"    译文: {sample.target_text[:30]}...")
            print(f"    领域: {sample.domain}")
            print(f"    难度: {sample.difficulty:.2f}")
            print(f"    质量: {sample.quality_score:.2f}")
        
        return True
        
    except Exception as e:
        print(f"✗ 数据加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_test_files():
    """
    清理测试文件
    """
    print("\n=== 清理测试文件 ===")
    
    import shutil
    
    test_dirs = ["test_demo_pairs"]
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            try:
                shutil.rmtree(test_dir)
                print(f"✓ 已删除测试目录: {test_dir}")
            except Exception as e:
                print(f"⚠️ 删除测试目录失败: {e}")

def main():
    """
    主测试函数
    """
    print("增强版Transformers模块测试")
    print("=" * 50)
    
    test_results = []
    module = None
    
    # 1. 测试依赖库导入
    result = test_imports()
    test_results.append(("依赖库导入", result))
    
    if not result:
        print("\n❌ 依赖库测试失败，请安装必要的依赖")
        print("运行: pip install transformers torch sacrebleu numpy")
        return
    
    # 2. 测试模块导入
    result = test_module_import()
    test_results.append(("模块导入", result))
    
    if not result:
        print("\n❌ 模块导入失败，请检查文件是否存在")
        return
    
    # 3. 测试配置文件
    result = test_config_file()
    test_results.append(("配置文件", result))
    
    # 4. 测试数据结构
    result = test_data_structures()
    test_results.append(("数据结构", result))
    
    # 5. 测试模块初始化
    result, module = test_module_initialization()
    test_results.append(("模块初始化", result))
    
    if result and module:
        # 6. 测试基础翻译
        result = test_basic_translation(module)
        test_results.append(("基础翻译", result))
        
        # 7. 测试演示数据创建
        result = test_demo_data_creation()
        test_results.append(("演示数据创建", result))
        
        if result:
            # 8. 测试数据加载
            result = test_data_loading(module)
            test_results.append(("数据加载", result))
    
    # 显示测试结果总结
    print("\n" + "=" * 50)
    print("测试结果总结")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name:<15} {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！模块可以正常使用。")
    else:
        print("⚠️ 部分测试失败，请检查相关配置。")
    
    # 清理测试文件
    cleanup_test_files()

if __name__ == "__main__":
    main()