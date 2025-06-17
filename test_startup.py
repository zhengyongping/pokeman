#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动测试脚本
验证NLLB学习系统是否正常工作
"""

import os
import sys
import json
from datetime import datetime

def test_environment():
    """测试环境"""
    print("=" * 50)
    print("NLLB学习系统启动测试")
    print("=" * 50)
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    
    # 检查当前目录
    print(f"当前目录: {os.getcwd()}")
    
    # 检查必要文件
    required_files = [
        "nllb_learning_module.py",
        "nllb_config.json",
        "individual_pairs"
    ]
    
    print("\n检查必要文件:")
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (缺失)")
    
    return True

def test_imports():
    """测试导入"""
    print("\n检查依赖库:")
    
    try:
        import torch
        print(f"✓ PyTorch {torch.__version__}")
    except ImportError:
        print("✗ PyTorch (未安装)")
        return False
    
    try:
        import transformers
        print(f"✓ Transformers {transformers.__version__}")
    except ImportError:
        print("✗ Transformers (未安装)")
        return False
    
    try:
        from nllb_learning_module import NLLBLearningModule
        print("✓ NLLB学习模块")
    except ImportError as e:
        print(f"✗ NLLB学习模块 ({e})")
        return False
    
    return True

def test_config():
    """测试配置"""
    print("\n检查配置文件:")
    
    try:
        with open("nllb_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        model_name = config.get("model", {}).get("model_name", "未知")
        print(f"✓ 配置文件加载成功")
        print(f"  模型: {model_name}")
        
        return True
        
    except Exception as e:
        print(f"✗ 配置文件错误: {e}")
        return False

def test_data():
    """测试数据"""
    print("\n检查数据目录:")
    
    data_dir = "individual_pairs"
    if not os.path.exists(data_dir):
        print(f"✗ 数据目录 {data_dir} 不存在")
        return False
    
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    
    if not json_files:
        print(f"✗ 数据目录 {data_dir} 中没有JSON文件")
        return False
    
    print(f"✓ 找到 {len(json_files)} 个数据文件")
    
    # 检查第一个文件的格式
    try:
        with open(os.path.join(data_dir, json_files[0]), "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if "source" in first_item and "target" in first_item:
                print("✓ 数据格式正确")
                return True
        
        print("✗ 数据格式不正确")
        return False
        
    except Exception as e:
        print(f"✗ 数据文件读取错误: {e}")
        return False

def test_module_initialization():
    """测试模块初始化"""
    print("\n测试模块初始化:")
    
    try:
        from nllb_learning_module import NLLBLearningModule
        
        # 创建模块实例
        module = NLLBLearningModule("nllb_config.json")
        print(f"✓ 模块创建成功")
        print(f"  设备: {module.device}")
        
        # 测试数据加载
        examples = module.load_translation_data("individual_pairs")
        print(f"✓ 数据加载成功: {len(examples)} 个翻译对")
        
        return True, module
        
    except Exception as e:
        print(f"✗ 模块初始化失败: {e}")
        return False, None

def run_simple_test(module):
    """运行简单测试"""
    print("\n运行简单功能测试:")
    
    try:
        # 测试语言检测
        lang = module._detect_language("Hello world")
        print(f"✓ 语言检测: {lang}")
        
        # 测试领域分类
        domain = module._classify_domain("Hello world")
        print(f"✓ 领域分类: {domain}")
        
        # 测试统计信息
        stats = module.learning_stats
        print(f"✓ 统计信息: {len(stats)} 项")
        
        return True
        
    except Exception as e:
        print(f"✗ 功能测试失败: {e}")
        return False

def main():
    """主函数"""
    # 环境测试
    if not test_environment():
        print("\n❌ 环境测试失败")
        return False
    
    # 导入测试
    if not test_imports():
        print("\n❌ 依赖库测试失败")
        return False
    
    # 配置测试
    if not test_config():
        print("\n❌ 配置测试失败")
        return False
    
    # 数据测试
    if not test_data():
        print("\n❌ 数据测试失败")
        return False
    
    # 模块测试
    success, module = test_module_initialization()
    if not success:
        print("\n❌ 模块初始化测试失败")
        return False
    
    # 功能测试
    if not run_simple_test(module):
        print("\n❌ 功能测试失败")
        return False
    
    # 所有测试通过
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！NLLB学习系统可以正常使用")
    print("=" * 50)
    
    print("\n下一步操作:")
    print("1. 运行完整学习: python run_nllb_learning.py")
    print("2. 运行演示程序: python demo_nllb_learning.py")
    print("3. 运行模块测试: python test_nllb_module.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n用户中断测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n测试过程中发生错误: {e}")
        sys.exit(1)