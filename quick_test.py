#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试NLLB模块
"""

try:
    print("开始测试...")
    
    # 测试基本导入
    import torch
    import transformers
    print("✓ 基础库导入成功")
    
    # 测试NLLB模块导入
    from nllb_learning_module import NLLBLearningModule
    print("✓ NLLB模块导入成功")
    
    # 测试配置文件
    import json
    with open('nllb_config.json', 'r') as f:
        config = json.load(f)
    print("✓ 配置文件读取成功")
    
    # 测试模块初始化
    module = NLLBLearningModule('nllb_config.json')
    print(f"✓ 模块初始化成功，设备: {module.device}")
    
    # 检查数据目录
    import os
    if os.path.exists('individual_pairs'):
        files = [f for f in os.listdir('individual_pairs') if f.endswith('.json')]
        print(f"✓ 找到 {len(files)} 个数据文件")
    else:
        print("✗ individual_pairs 目录不存在")
    
    print("\n所有测试通过！")
    
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()