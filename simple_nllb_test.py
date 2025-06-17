#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的NLLB模块测试脚本
自动运行基础测试，无需用户交互
"""

import sys
import os
import json
import traceback

def test_dependencies():
    """测试依赖库"""
    print("=== 依赖库测试 ===")
    
    required_packages = ['torch', 'transformers', 'sacrebleu', 'numpy']
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
        print(f"✓ 支持 {len(NLLB_LANGUAGE_CODES)} 种语言")
        return True
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
        traceback.print_exc()
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
        
    except Exception as e:
        print(f"✗ 配置文件错误: {e}")
        return False

def test_module_initialization():
    """测试模块初始化"""
    print("\n=== 模块初始化测试 ===")
    
    try:
        from nllb_learning_module import NLLBLearningModule
        
        nllb_module = NLLBLearningModule("nllb_config.json")
        print("✓ 模块实例创建成功")
        print(f"✓ 计算设备: {nllb_module.device}")
        print(f"✓ 配置加载成功")
        
        return True, nllb_module
        
    except Exception as e:
        print(f"✗ 模块初始化失败: {e}")
        traceback.print_exc()
        return False, None

def test_translation_example():
    """测试翻译样本创建"""
    print("\n=== 翻译样本测试 ===")
    
    try:
        from nllb_learning_module import NLLBTranslationExample
        
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
        
        return True
        
    except Exception as e:
        print(f"✗ 翻译样本创建失败: {e}")
        traceback.print_exc()
        return False

def test_data_creation_and_loading():
    """测试数据创建和加载"""
    print("\n=== 数据创建和加载测试 ===")
    
    try:
        # 创建测试数据
        test_dir = "test_nllb_data"
        os.makedirs(test_dir, exist_ok=True)
        
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
        
        print(f"✓ 测试数据创建成功: {len(test_data)} 个样本")
        
        # 测试数据加载
        from nllb_learning_module import NLLBLearningModule
        nllb_module = NLLBLearningModule("nllb_config.json")
        examples = nllb_module.load_translation_data(test_dir)
        
        if examples:
            print(f"✓ 数据加载成功: {len(examples)} 个样本")
            return True
        else:
            print("✗ 未加载到任何数据")
            return False
            
    except Exception as e:
        print(f"✗ 数据创建和加载失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("NLLB学习模块自动测试")
    print("=" * 50)
    
    tests = [
        ("依赖库测试", test_dependencies),
        ("模块导入测试", test_module_import),
        ("配置文件测试", test_config_file),
        ("模块初始化测试", lambda: test_module_initialization()[0]),
        ("翻译样本测试", test_translation_example),
        ("数据创建和加载测试", test_data_creation_and_loading)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n{test_name} 失败")
        except Exception as e:
            print(f"\n{test_name} 异常: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有测试通过！NLLB模块可以正常使用")
        print("\n下一步可以:")
        print("1. 运行演示脚本: python demo_nllb_learning.py")
        print("2. 使用individual_pairs数据进行学习")
    else:
        print(f"✗ {total - passed} 个测试失败，请检查错误信息")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)