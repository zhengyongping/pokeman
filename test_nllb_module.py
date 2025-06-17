#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NLLB学习模块测试脚本
验证NLLB模块的基本功能和兼容性
"""

import sys
import os
import json
from datetime import datetime

def test_dependencies():
    """测试依赖库"""
    print("=== 依赖库测试 ===")
    
    required_packages = [
        'torch',
        'transformers', 
        'sacrebleu',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} - 已安装")
        except ImportError:
            print(f"✗ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺少依赖库: {', '.join(missing_packages)}")
        print("请运行: pip install torch transformers sacrebleu numpy")
        return False
    
    print("所有依赖库已安装")
    return True

def test_module_import():
    """测试模块导入"""
    print("\n=== 模块导入测试 ===")
    
    try:
        from nllb_learning_module import (
            NLLBLearningModule, 
            NLLBTranslationExample, 
            NLLB_LANGUAGE_CODES
        )
        print("✓ NLLB学习模块导入成功")
        
        # 测试语言代码
        print(f"✓ 支持 {len(NLLB_LANGUAGE_CODES)} 种语言")
        print(f"  语言列表: {list(NLLB_LANGUAGE_CODES.keys())[:5]}...")
        
        return True
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def test_config_file():
    """测试配置文件"""
    print("\n=== 配置文件测试 ===")
    
    config_path = "nllb_config.json"
    
    if not os.path.exists(config_path):
        print(f"✗ 配置文件 {config_path} 不存在")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_sections = ['model', 'training', 'data', 'languages']
        
        for section in required_sections:
            if section in config:
                print(f"✓ 配置节 '{section}' 存在")
            else:
                print(f"✗ 配置节 '{section}' 缺失")
                return False
        
        print("✓ 配置文件格式正确")
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ 配置文件格式错误: {e}")
        return False
    except Exception as e:
        print(f"✗ 读取配置文件失败: {e}")
        return False

def test_module_initialization():
    """测试模块初始化"""
    print("\n=== 模块初始化测试 ===")
    
    try:
        from nllb_learning_module import NLLBLearningModule
        
        # 创建模块实例
        nllb_module = NLLBLearningModule("nllb_config.json")
        print("✓ 模块实例创建成功")
        
        # 检查设备设置
        device = nllb_module.device
        print(f"✓ 计算设备: {device}")
        
        # 检查配置加载
        config = nllb_module.config
        print(f"✓ 配置加载成功: {len(config)} 个配置节")
        
        return True, nllb_module
        
    except Exception as e:
        print(f"✗ 模块初始化失败: {e}")
        return False, None

def test_model_initialization(nllb_module):
    """测试模型初始化（可选，需要网络连接）"""
    print("\n=== 模型初始化测试 ===")
    
    try:
        # 注意：这会下载模型，可能需要较长时间
        print("正在初始化NLLB模型（可能需要下载，请耐心等待）...")
        nllb_module.initialize_model(source_lang="english", target_lang="chinese")
        
        if nllb_module.model is not None and nllb_module.tokenizer is not None:
            print("✓ NLLB模型初始化成功")
            return True
        else:
            print("✗ 模型或tokenizer未正确初始化")
            return False
            
    except Exception as e:
        print(f"✗ 模型初始化失败: {e}")
        print("  这可能是由于网络连接问题或模型下载失败")
        return False

def test_translation_example():
    """测试翻译样本创建"""
    print("\n=== 翻译样本测试 ===")
    
    try:
        from nllb_learning_module import NLLBTranslationExample
        
        # 创建测试样本
        example = NLLBTranslationExample(
            source_text="Hello world",
            target_text="你好世界",
            source_lang="english",
            target_lang="chinese",
            domain="general"
        )
        
        print("✓ 翻译样本创建成功")
        print(f"  源文本: {example.source_text}")
        print(f"  目标文本: {example.target_text}")
        print(f"  语言对: {example.source_lang} -> {example.target_lang}")
        print(f"  领域: {example.domain}")
        
        return True
        
    except Exception as e:
        print(f"✗ 翻译样本创建失败: {e}")
        return False

def test_demo_data_creation():
    """测试演示数据创建"""
    print("\n=== 演示数据创建测试 ===")
    
    try:
        # 创建测试数据目录
        test_dir = "test_nllb_data"
        os.makedirs(test_dir, exist_ok=True)
        
        # 创建测试数据
        test_data = [
            {
                "source": "Hello",
                "target": "你好",
                "source_lang": "english",
                "target_lang": "chinese"
            },
            {
                "source": "Thank you",
                "target": "谢谢",
                "source_lang": "english",
                "target_lang": "chinese"
            }
        ]
        
        test_file = os.path.join(test_dir, "test_data.json")
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 测试数据创建成功: {test_file}")
        print(f"  包含 {len(test_data)} 个样本")
        
        return True, test_dir
        
    except Exception as e:
        print(f"✗ 测试数据创建失败: {e}")
        return False, None

def test_data_loading(nllb_module, test_dir):
    """测试数据加载"""
    print("\n=== 数据加载测试 ===")
    
    if not nllb_module or not test_dir:
        print("✗ 缺少必要的测试条件")
        return False
    
    try:
        examples = nllb_module.load_translation_data(test_dir)
        
        if examples:
            print(f"✓ 数据加载成功: {len(examples)} 个样本")
            
            # 显示第一个样本
            if examples:
                first_example = examples[0]
                print(f"  示例样本:")
                print(f"    源文本: {first_example.source_text}")
                print(f"    目标文本: {first_example.target_text}")
                print(f"    语言对: {first_example.source_lang} -> {first_example.target_lang}")
            
            return True
        else:
            print("✗ 未加载到任何数据")
            return False
            
    except Exception as e:
        print(f"✗ 数据加载失败: {e}")
        return False

def run_basic_tests():
    """运行基础测试（不需要模型下载）"""
    print("NLLB学习模块基础测试")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # 1. 依赖库测试
    total_tests += 1
    if test_dependencies():
        tests_passed += 1
    
    # 2. 模块导入测试
    total_tests += 1
    if test_module_import():
        tests_passed += 1
    
    # 3. 配置文件测试
    total_tests += 1
    if test_config_file():
        tests_passed += 1
    
    # 4. 模块初始化测试
    total_tests += 1
    success, nllb_module = test_module_initialization()
    if success:
        tests_passed += 1
    
    # 5. 翻译样本测试
    total_tests += 1
    if test_translation_example():
        tests_passed += 1
    
    # 6. 演示数据创建测试
    total_tests += 1
    success, test_dir = test_demo_data_creation()
    if success:
        tests_passed += 1
    
    # 7. 数据加载测试
    total_tests += 1
    if test_data_loading(nllb_module, test_dir):
        tests_passed += 1
    
    # 测试结果
    print("\n" + "=" * 50)
    print(f"基础测试完成: {tests_passed}/{total_tests} 通过")
    
    if tests_passed == total_tests:
        print("✓ 所有基础测试通过！")
        return True
    else:
        print(f"✗ {total_tests - tests_passed} 个测试失败")
        return False

def run_full_tests():
    """运行完整测试（包括模型下载）"""
    print("\nNLLB学习模块完整测试")
    print("=" * 50)
    print("警告：完整测试将下载NLLB模型（约600MB），可能需要较长时间")
    
    response = input("是否继续完整测试？(y/N): ")
    if response.lower() != 'y':
        print("跳过完整测试")
        return
    
    # 先运行基础测试
    if not run_basic_tests():
        print("基础测试失败，跳过完整测试")
        return
    
    # 模型初始化测试
    print("\n开始模型初始化测试...")
    from nllb_learning_module import NLLBLearningModule
    nllb_module = NLLBLearningModule("nllb_config.json")
    
    if test_model_initialization(nllb_module):
        print("✓ 完整测试通过！")
        
        # 可选：测试简单翻译
        try:
            translation = nllb_module.translate_text("Hello", "english", "chinese")
            print(f"✓ 翻译测试: 'Hello' -> '{translation}'")
        except Exception as e:
            print(f"✗ 翻译测试失败: {e}")
    else:
        print("✗ 完整测试失败")

def main():
    """主测试函数"""
    print("NLLB学习模块测试工具")
    print("=" * 60)
    
    # 运行基础测试
    basic_success = run_basic_tests()
    
    if basic_success:
        print("\n基础功能测试通过！")
        print("\n可选操作:")
        print("1. 运行完整测试（包括模型下载）")
        print("2. 运行演示脚本")
        print("3. 退出")
        
        choice = input("\n请选择 (1/2/3): ")
        
        if choice == '1':
            run_full_tests()
        elif choice == '2':
            print("\n运行演示脚本...")
            print("请执行: python demo_nllb_learning.py")
        else:
            print("测试完成")
    else:
        print("\n基础测试失败，请检查环境配置")

if __name__ == "__main__":
    main()