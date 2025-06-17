#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据格式转换工具
将individual_pairs目录中的文件转换为NLLB学习模块可读取的格式
"""

import os
import json
import glob
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataFormatConverter:
    """数据格式转换器"""
    
    def __init__(self, input_dir: str = "individual_pairs", output_dir: str = "individual_pairs_formatted"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.supported_formats = [
            # 原始格式（英文-中文键值对）
            ['english', 'chinese'],
            ['en', 'zh'],
            ['eng', 'chn'],
            # NLLB标准格式
            ['source', 'target'],
            # 其他可能的格式
            ['original', 'translation'],
            ['text', 'translated_text']
        ]
        
    def detect_format(self, data: Dict) -> Optional[List[str]]:
        """检测数据格式"""
        for format_pair in self.supported_formats:
            if all(key in data for key in format_pair):
                return format_pair
        return None
    
    def convert_single_file(self, input_file: str, output_file: str) -> bool:
        """转换单个文件"""
        try:
            logger.info(f"转换文件: {input_file} -> {output_file}")
            
            # 读取输入文件
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 处理不同的数据结构
            if isinstance(data, list):
                # 如果是数组，转换每个元素
                converted_data = []
                for item in data:
                    converted_item = self.convert_item(item)
                    if converted_item:
                        converted_data.append(converted_item)
            elif isinstance(data, dict):
                # 如果是单个对象，直接转换
                converted_item = self.convert_item(data)
                if converted_item:
                    converted_data = [converted_item]
                else:
                    converted_data = []
            else:
                logger.error(f"不支持的数据格式: {type(data)}")
                return False
            
            if not converted_data:
                logger.warning(f"文件 {input_file} 没有有效的翻译对")
                return False
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # 写入输出文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(converted_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"成功转换 {len(converted_data)} 个翻译对")
            return True
            
        except Exception as e:
            logger.error(f"转换文件 {input_file} 时出错: {e}")
            return False
    
    def convert_item(self, item: Dict) -> Optional[Dict]:
        """转换单个数据项"""
        try:
            # 检测格式
            format_pair = self.detect_format(item)
            
            if not format_pair:
                logger.warning(f"无法识别数据格式: {list(item.keys())}")
                return None
            
            source_key, target_key = format_pair
            source_text = item[source_key]
            target_text = item[target_key]
            
            # 验证文本内容
            if not source_text or not target_text:
                logger.warning("源文本或目标文本为空")
                return None
            
            # 检测语言
            source_lang = self.detect_language(source_text)
            target_lang = self.detect_language(target_text)
            
            # 创建标准格式
            converted_item = {
                "source": str(source_text).strip(),
                "target": str(target_text).strip(),
                "source_lang": source_lang,
                "target_lang": target_lang
            }
            
            # 保留其他元数据
            for key, value in item.items():
                if key not in [source_key, target_key] and key not in converted_item:
                    converted_item[f"metadata_{key}"] = value
            
            return converted_item
            
        except Exception as e:
            logger.error(f"转换数据项时出错: {e}")
            return None
    
    def detect_language(self, text: str) -> str:
        """简单的语言检测"""
        import re
        
        # 检测中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        # 检测日文字符
        japanese_chars = len(re.findall(r'[\u3040-\u309f\u30a0-\u30ff]', text))
        # 检测韩文字符
        korean_chars = len(re.findall(r'[\uac00-\ud7af]', text))
        
        total_chars = len(text)
        
        if total_chars == 0:
            return "unknown"
        
        # 计算各语言字符比例
        chinese_ratio = chinese_chars / total_chars
        japanese_ratio = japanese_chars / total_chars
        korean_ratio = korean_chars / total_chars
        
        # 判断语言
        if chinese_ratio > 0.3:
            return "chinese"
        elif japanese_ratio > 0.3:
            return "japanese"
        elif korean_ratio > 0.3:
            return "korean"
        else:
            return "english"  # 默认为英文
    
    def convert_directory(self) -> bool:
        """转换整个目录"""
        try:
            if not os.path.exists(self.input_dir):
                logger.error(f"输入目录不存在: {self.input_dir}")
                return False
            
            # 查找所有JSON文件
            json_files = glob.glob(os.path.join(self.input_dir, "*.json"))
            
            if not json_files:
                logger.warning(f"在 {self.input_dir} 中没有找到JSON文件")
                return False
            
            logger.info(f"找到 {len(json_files)} 个JSON文件")
            
            # 创建输出目录
            os.makedirs(self.output_dir, exist_ok=True)
            
            success_count = 0
            
            for input_file in json_files:
                filename = os.path.basename(input_file)
                output_file = os.path.join(self.output_dir, filename)
                
                if self.convert_single_file(input_file, output_file):
                    success_count += 1
            
            logger.info(f"转换完成: {success_count}/{len(json_files)} 个文件成功")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"转换目录时出错: {e}")
            return False
    
    def create_sample_data(self) -> bool:
        """创建示例数据用于测试"""
        try:
            # 创建输入目录
            os.makedirs(self.input_dir, exist_ok=True)
            
            # 示例数据（不同格式）
            sample_data = [
                # 格式1: english/chinese
                {
                    "filename": "sample_001.json",
                    "data": {
                        "english": "Hello, how are you?",
                        "chinese": "你好，你好吗？"
                    }
                },
                # 格式2: source/target
                {
                    "filename": "sample_002.json",
                    "data": {
                        "source": "Thank you very much.",
                        "target": "非常感谢。"
                    }
                },
                # 格式3: 数组格式
                {
                    "filename": "sample_003.json",
                    "data": [
                        {
                            "en": "Good morning",
                            "zh": "早上好"
                        },
                        {
                            "en": "Good night",
                            "zh": "晚安"
                        }
                    ]
                }
            ]
            
            for sample in sample_data:
                file_path = os.path.join(self.input_dir, sample["filename"])
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(sample["data"], f, ensure_ascii=False, indent=2)
                logger.info(f"创建示例文件: {file_path}")
            
            logger.info(f"成功创建 {len(sample_data)} 个示例文件")
            return True
            
        except Exception as e:
            logger.error(f"创建示例数据时出错: {e}")
            return False
    
    def validate_output(self) -> bool:
        """验证输出格式"""
        try:
            if not os.path.exists(self.output_dir):
                logger.error(f"输出目录不存在: {self.output_dir}")
                return False
            
            json_files = glob.glob(os.path.join(self.output_dir, "*.json"))
            
            if not json_files:
                logger.warning(f"输出目录中没有JSON文件")
                return False
            
            valid_count = 0
            
            for file_path in json_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if not isinstance(data, list):
                        logger.error(f"文件 {file_path} 不是数组格式")
                        continue
                    
                    valid_items = 0
                    for item in data:
                        required_keys = ['source', 'target', 'source_lang', 'target_lang']
                        if all(key in item for key in required_keys):
                            valid_items += 1
                        else:
                            logger.warning(f"文件 {file_path} 中的项缺少必需字段")
                    
                    if valid_items > 0:
                        valid_count += 1
                        logger.info(f"文件 {file_path} 验证通过: {valid_items} 个有效项")
                    
                except Exception as e:
                    logger.error(f"验证文件 {file_path} 时出错: {e}")
            
            logger.info(f"验证完成: {valid_count}/{len(json_files)} 个文件有效")
            return valid_count > 0
            
        except Exception as e:
            logger.error(f"验证输出时出错: {e}")
            return False

def main():
    """主函数"""
    print("数据格式转换工具")
    print("=" * 50)
    
    converter = DataFormatConverter()
    
    # 检查输入目录
    if not os.path.exists(converter.input_dir):
        print(f"输入目录 {converter.input_dir} 不存在")
        print("是否创建示例数据进行测试？(y/N): ", end="")
        response = input().strip().lower()
        
        if response == 'y':
            print("\n创建示例数据...")
            if converter.create_sample_data():
                print("示例数据创建成功")
            else:
                print("示例数据创建失败")
                return
        else:
            print("请先准备数据文件")
            return
    
    # 执行转换
    print(f"\n开始转换 {converter.input_dir} 目录中的文件...")
    
    if converter.convert_directory():
        print("\n转换完成！")
        
        # 验证输出
        print("\n验证输出格式...")
        if converter.validate_output():
            print("\n✓ 所有文件格式正确")
            print(f"\n转换后的文件保存在: {converter.output_dir}")
            print("\n现在可以使用NLLB学习模块读取这些文件了")
            print("\n使用方法:")
            print(f"1. 将 {converter.output_dir} 重命名为 individual_pairs")
            print("2. 运行: python run_nllb_learning.py")
        else:
            print("\n✗ 输出格式验证失败")
    else:
        print("\n转换失败")

if __name__ == "__main__":
    main()