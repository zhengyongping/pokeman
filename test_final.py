#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试脚本 - 验证NLLB学习系统
"""

import sys
import os
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_final.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def test_nllb_system():
    """测试NLLB学习系统"""
    logger.info("=== NLLB学习系统最终测试 ===")
    
    try:
        # 导入模块
        logger.info("1. 导入NLLB学习模块...")
        from nllb_learning_module import NLLBLearningModule
        logger.info("✓ 模块导入成功")
        
        # 创建实例
        logger.info("2. 创建学习模块实例...")
        nllb_module = NLLBLearningModule()
        logger.info("✓ 实例创建成功")
        
        # 检查配置
        logger.info("3. 检查配置...")
        logger.info(f"模型名称: {nllb_module.model_config.model_name}")
        logger.info(f"设备: {nllb_module.device}")
        logger.info("✓ 配置检查完成")
        
        # 检查数据目录
        data_dir = "individual_pairs"
        logger.info(f"4. 检查数据目录: {data_dir}")
        if os.path.exists(data_dir):
            files = os.listdir(data_dir)
            logger.info(f"找到 {len(files)} 个数据文件")
            logger.info("✓ 数据目录存在")
        else:
            logger.warning("⚠ 数据目录不存在")
        
        # 测试基本功能
        logger.info("5. 测试基本功能...")
        
        # 语言检测
        test_text = "Hello world"
        detected_lang = nllb_module._detect_language(test_text)
        logger.info(f"语言检测: '{test_text}' -> {detected_lang}")
        
        # 领域分类
        domain = nllb_module._classify_domain(test_text)
        logger.info(f"领域分类: '{test_text}' -> {domain}")
        
        logger.info("✓ 基本功能测试完成")
        
        # 统计信息
        logger.info("6. 学习统计信息:")
        for key, value in nllb_module.learning_stats.items():
            logger.info(f"  {key}: {value}")
        
        logger.info("=== 测试完成 ===")
        return True
        
    except Exception as e:
        logger.error(f"测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_nllb_system()
    if success:
        print("\n🎉 NLLB学习系统测试通过！")
        print("系统已准备就绪，可以开始学习任务。")
    else:
        print("\n❌ 测试失败，请检查错误日志。")
    
    sys.exit(0 if success else 1)