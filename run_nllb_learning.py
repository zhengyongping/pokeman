#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NLLB学习模块运行脚本
用于学习individual_pairs目录中的翻译对数据
"""

import os
import sys
import json
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nllb_learning.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """检查依赖库"""
    logger.info("检查依赖库...")
    
    required_packages = {
        'torch': 'PyTorch',
        'transformers': 'Hugging Face Transformers',
        'sacrebleu': 'SacreBLEU',
        'numpy': 'NumPy'
    }
    
    missing = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            logger.info(f"✓ {name} 已安装")
        except ImportError:
            logger.error(f"✗ {name} 未安装")
            missing.append(package)
    
    if missing:
        logger.error(f"缺少依赖库: {', '.join(missing)}")
        logger.error("请运行: pip install torch transformers sacrebleu numpy")
        return False
    
    logger.info("所有依赖库检查通过")
    return True

def check_data_directory():
    """检查数据目录"""
    data_dir = "individual_pairs"
    
    if not os.path.exists(data_dir):
        logger.error(f"数据目录 {data_dir} 不存在")
        return False
    
    # 检查JSON文件
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    
    if not json_files:
        logger.error(f"数据目录 {data_dir} 中没有找到JSON文件")
        return False
    
    logger.info(f"找到 {len(json_files)} 个数据文件: {json_files[:3]}{'...' if len(json_files) > 3 else ''}")
    return True

def check_config_file():
    """检查配置文件"""
    config_file = "nllb_config.json"
    
    if not os.path.exists(config_file):
        logger.error(f"配置文件 {config_file} 不存在")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_sections = ['model', 'training', 'data', 'languages']
        for section in required_sections:
            if section not in config:
                logger.error(f"配置文件缺少 '{section}' 节")
                return False
        
        logger.info("配置文件检查通过")
        return True
        
    except Exception as e:
        logger.error(f"配置文件错误: {e}")
        return False

def run_nllb_learning():
    """运行NLLB学习模块"""
    logger.info("开始NLLB学习过程...")
    
    try:
        # 导入NLLB模块
        from nllb_learning_module import NLLBLearningModule
        logger.info("NLLB模块导入成功")
        
        # 创建学习模块实例
        nllb_module = NLLBLearningModule("nllb_config.json")
        logger.info(f"模块初始化成功，使用设备: {nllb_module.device}")
        
        # 加载翻译数据
        logger.info("加载翻译数据...")
        examples = nllb_module.load_translation_data("individual_pairs")
        
        if not examples:
            logger.error("未加载到任何翻译数据")
            return False
        
        logger.info(f"成功加载 {len(examples)} 个翻译样本")
        
        # 数据已在load_translation_data中自动分割
        logger.info("获取分割后的数据集...")
        train_examples = nllb_module.training_data
        val_examples = nllb_module.validation_data
        test_examples = nllb_module.test_data
        
        logger.info(f"数据分割完成:")
        logger.info(f"  训练集: {len(train_examples)} 样本")
        logger.info(f"  验证集: {len(val_examples)} 样本")
        logger.info(f"  测试集: {len(test_examples)} 样本")
        
        # 初始化模型（使用第一个样本的语言对）
        if examples:
            first_example = examples[0]
            source_lang = first_example.source_lang
            target_lang = first_example.target_lang
            
            logger.info(f"初始化NLLB模型: {source_lang} -> {target_lang}")
            nllb_module.initialize_model(source_lang, target_lang)
            logger.info("模型初始化完成")
        
        # 进行模型微调（如果配置允许）
        if nllb_module.config.get('training', {}).get('enable_fine_tuning', False):
            logger.info("开始模型微调...")
            nllb_module.fine_tune_model(train_examples, val_examples)
            logger.info("模型微调完成")
        else:
            logger.info("跳过模型微调（配置中未启用）")
        
        # 模型评估
        logger.info("开始模型评估...")
        evaluation_results = nllb_module.evaluate_model()
        
        logger.info("评估结果:")
        for metric, value in evaluation_results.items():
            logger.info(f"  {metric}: {value}")
        
        # 测试翻译功能
        logger.info("测试翻译功能...")
        test_texts = ["Hello", "Thank you", "Good morning"]
        
        for text in test_texts:
            try:
                translation = nllb_module.translate_text(text, source_lang, target_lang)
                logger.info(f"  '{text}' -> '{translation}'")
            except Exception as e:
                logger.warning(f"翻译 '{text}' 失败: {e}")
        
        # 保存学习报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"nllb_learning_report_{timestamp}.json"
        
        report = {
            "timestamp": timestamp,
            "data_summary": {
                "total_examples": len(examples),
                "train_examples": len(train_examples),
                "val_examples": len(val_examples),
                "test_examples": len(test_examples)
            },
            "model_info": {
                "source_language": source_lang,
                "target_language": target_lang,
                "device": str(nllb_module.device)
            },
            "evaluation_results": evaluation_results,
            "learning_statistics": nllb_module.learning_stats
        }
        
        report_file = nllb_module.save_learning_report(report_file)
        logger.info(f"学习报告已保存: {report_file}")
        
        logger.info("NLLB学习过程完成！")
        return True
        
    except Exception as e:
        logger.error(f"NLLB学习过程失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("NLLB翻译学习系统")
    logger.info("=" * 60)
    
    # 检查环境
    logger.info("步骤 1: 环境检查")
    if not check_dependencies():
        logger.error("依赖库检查失败")
        return False
    
    if not check_data_directory():
        logger.error("数据目录检查失败")
        return False
    
    if not check_config_file():
        logger.error("配置文件检查失败")
        return False
    
    logger.info("环境检查通过")
    
    # 运行学习过程
    logger.info("\n步骤 2: 开始学习过程")
    success = run_nllb_learning()
    
    if success:
        logger.info("\n=== 学习完成 ===")
        logger.info("NLLB模型已成功学习individual_pairs数据")
        logger.info("可以查看生成的学习报告了解详细结果")
    else:
        logger.error("\n=== 学习失败 ===")
        logger.error("请检查错误日志并解决问题")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n用户中断了学习过程")
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序异常退出: {e}")
        sys.exit(1)