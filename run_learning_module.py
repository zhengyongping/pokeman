#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行学习模块 - 学习individual_pairs中的翻译对
"""

import os
import sys
import json
from datetime import datetime

def check_dependencies():
    """检查依赖库"""
    try:
        import torch
        import transformers
        import sacrebleu
        print("✓ 所有依赖库已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖库: {e}")
        print("请运行: pip install transformers torch sacrebleu")
        return False

def check_data():
    """检查数据目录"""
    pairs_dir = "individual_pairs"
    if not os.path.exists(pairs_dir):
        print(f"✗ 数据目录 {pairs_dir} 不存在")
        return False
    
    json_files = [f for f in os.listdir(pairs_dir) if f.endswith('.json')]
    if not json_files:
        print(f"✗ {pairs_dir} 目录中没有JSON文件")
        return False
    
    print(f"✓ 找到 {len(json_files)} 个翻译对文件")
    return True

def run_learning():
    """运行学习模块"""
    print("\n=== 开始运行学习模块 ===")
    
    try:
        from enhanced_transformers_module import EnhancedTransformersModule
        
        # 创建学习模块
        print("正在初始化学习模块...")
        module = EnhancedTransformersModule(
            config_path="transformers_config.json",
            model_key="mt5_small"
        )
        
        # 加载翻译对数据
        print("正在加载individual_pairs中的翻译对...")
        module.load_translation_data()
        
        if not module.training_examples:
            print("✗ 没有找到有效的训练数据")
            return False
        
        print(f"✓ 成功加载 {len(module.training_examples)} 个训练样本")
        print(f"  验证集: {len(module.validation_examples)} 个")
        print(f"  测试集: {len(module.test_examples)} 个")
        
        # 显示数据统计
        print("\n=== 数据统计 ===")
        domains = {}
        for example in module.training_examples:
            domain = example.domain
            domains[domain] = domains.get(domain, 0) + 1
        
        for domain, count in domains.items():
            print(f"  {domain}: {count} 个样本")
        
        # 微调模型
        print("\n=== 开始模型微调 ===")
        print("使用demo配置进行快速训练...")
        module.fine_tune_model(config_name="demo")
        
        # 评估模型
        print("\n=== 模型评估 ===")
        results = module.comprehensive_evaluate()
        
        # 显示评估结果
        if results:
            print("评估结果:")
            for metric, value in results.items():
                if isinstance(value, float):
                    print(f"  {metric}: {value:.4f}")
                else:
                    print(f"  {metric}: {value}")
        
        # 测试翻译
        print("\n=== 测试翻译 ===")
        test_texts = [
            "Giratina-O is a powerful Ghost/Dragon-type Pokemon.",
            "This Pokemon has excellent offensive capabilities.",
            "The strategy focuses on maximizing damage output."
        ]
        
        for text in test_texts:
            try:
                translation = module.translate_text(text)
                print(f"原文: {text}")
                print(f"译文: {translation}")
                print()
            except Exception as e:
                print(f"翻译失败: {e}")
        
        # 保存学习报告
        print("=== 保存学习报告 ===")
        report_file = module.save_comprehensive_report()
        print(f"学习报告已保存到: {report_file}")
        
        return True
        
    except Exception as e:
        print(f"✗ 学习过程出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=== 翻译学习模块 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查环境
    if not check_dependencies():
        return
    
    if not check_data():
        return
    
    # 运行学习
    success = run_learning()
    
    if success:
        print("\n✓ 学习模块运行完成!")
    else:
        print("\n✗ 学习模块运行失败!")

if __name__ == "__main__":
    main()