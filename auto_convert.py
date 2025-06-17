#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化数据格式转换脚本
"""

import os
import sys
import json
import glob
import shutil
from typing import Dict, List, Any, Optional

def detect_language(text: str) -> str:
    """简单的语言检测"""
    import re
    
    # 检测中文字符
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.strip())
    
    if total_chars == 0:
        return "unknown"
    
    # 如果中文字符超过30%，认为是中文
    if chinese_chars / total_chars > 0.3:
        return "chinese"
    else:
        return "english"  # 默认为英文

def convert_item(item: Dict) -> Optional[Dict]:
    """转换单个数据项为标准格式"""
    # 支持的字段映射
    source_fields = ['source', 'english', 'en', 'eng', 'original', 'text']
    target_fields = ['target', 'chinese', 'zh', 'chn', 'translation', 'translated_text']
    
    source_text = None
    target_text = None
    
    # 查找源文本
    for field in source_fields:
        if field in item and item[field]:
            source_text = str(item[field]).strip()
            break
    
    # 查找目标文本
    for field in target_fields:
        if field in item and item[field]:
            target_text = str(item[field]).strip()
            break
    
    if not source_text or not target_text:
        return None
    
    # 检测语言
    source_lang = detect_language(source_text)
    target_lang = detect_language(target_text)
    
    return {
        "source": source_text,
        "target": target_text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }

def convert_file(input_file: str, output_file: str) -> bool:
    """转换单个文件"""
    try:
        print(f"转换: {input_file}")
        
        # 读取文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        converted_items = []
        
        # 处理不同的数据结构
        if isinstance(data, dict):
            # 单个翻译对
            converted = convert_item(data)
            if converted:
                converted_items.append(converted)
        elif isinstance(data, list):
            # 多个翻译对
            for item in data:
                if isinstance(item, dict):
                    converted = convert_item(item)
                    if converted:
                        converted_items.append(converted)
        
        if not converted_items:
            print(f"  警告: 文件 {input_file} 没有有效的翻译对")
            return False
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 写入转换后的数据
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(converted_items, f, ensure_ascii=False, indent=2)
        
        print(f"  成功: {len(converted_items)} 个翻译对")
        return True
        
    except Exception as e:
        print(f"  错误: {e}")
        return False

def create_sample_data(output_dir: str = "individual_pairs") -> bool:
    """创建示例数据"""
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # 示例数据
        samples = [
            # 格式1: english/chinese
            {
                "filename": "pair_001.json",
                "data": [
                    {
                        "english": "Hello, how are you?",
                        "chinese": "你好，你好吗？"
                    },
                    {
                        "english": "What's your name?",
                        "chinese": "你叫什么名字？"
                    }
                ]
            },
            # 格式2: 宝可梦相关
            {
                "filename": "pair_002.json",
                "data": [
                    {
                        "english": "Pikachu is an Electric-type Pokemon.",
                        "chinese": "皮卡丘是电属性宝可梦。"
                    },
                    {
                        "english": "Charizard can learn Fire-type moves.",
                        "chinese": "喷火龙可以学习火属性招式。"
                    },
                    {
                        "english": "Pokemon trainers catch Pokemon with Pokeballs.",
                        "chinese": "宝可梦训练师用精灵球捕捉宝可梦。"
                    }
                ]
            },
            # 格式3: 日常对话
            {
                "filename": "pair_003.json",
                "data": [
                    {
                        "source": "Good morning!",
                        "target": "早上好！"
                    },
                    {
                        "source": "Thank you very much.",
                        "target": "非常感谢。"
                    },
                    {
                        "source": "See you tomorrow.",
                        "target": "明天见。"
                    }
                ]
            }
        ]
        
        for sample in samples:
            file_path = os.path.join(output_dir, sample["filename"])
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(sample["data"], f, ensure_ascii=False, indent=2)
            print(f"创建示例文件: {file_path}")
        
        print(f"\n成功创建 {len(samples)} 个示例文件在 {output_dir} 目录")
        return True
        
    except Exception as e:
        print(f"创建示例数据失败: {e}")
        return False

def convert_directory(input_dir: str, output_dir: str) -> int:
    """转换整个目录"""
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录 {input_dir} 不存在")
        return 0
    
    # 查找所有JSON文件
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    
    if not json_files:
        print(f"警告: 在 {input_dir} 中没有找到JSON文件")
        return 0
    
    print(f"找到 {len(json_files)} 个JSON文件")
    print("-" * 50)
    
    success_count = 0
    
    for input_file in json_files:
        filename = os.path.basename(input_file)
        output_file = os.path.join(output_dir, filename)
        
        if convert_file(input_file, output_file):
            success_count += 1
    
    return success_count

def main():
    """主函数"""
    print("自动化数据格式转换工具")
    print("=" * 50)
    
    # 设置目录
    input_dir = "individual_pairs"
    output_dir = "individual_pairs_formatted"
    
    # 步骤1: 检查或创建示例数据
    if not os.path.exists(input_dir) or not os.listdir(input_dir):
        print(f"\n步骤1: 创建示例数据到 {input_dir}")
        if not create_sample_data(input_dir):
            print("示例数据创建失败")
            return False
    else:
        print(f"\n步骤1: 发现现有数据在 {input_dir}")
    
    # 步骤2: 转换数据格式
    print(f"\n步骤2: 转换数据格式 {input_dir} -> {output_dir}")
    print("-" * 50)
    
    success_count = convert_directory(input_dir, output_dir)
    
    print("-" * 50)
    print(f"转换完成: {success_count} 个文件成功")
    
    if success_count > 0:
        # 步骤3: 自动替换目录
        print(f"\n步骤3: 替换原目录")
        try:
            # 备份原目录
            if os.path.exists(input_dir):
                backup_dir = f"{input_dir}_backup_{int(__import__('time').time())}"
                shutil.move(input_dir, backup_dir)
                print(f"原目录已备份为: {backup_dir}")
            
            # 重命名输出目录
            shutil.move(output_dir, input_dir)
            print(f"✓ {output_dir} 已重命名为 {input_dir}")
            
            print("\n✓ 数据格式转换完成！")
            print("现在可以运行: python run_nllb_learning.py")
            return True
            
        except Exception as e:
            print(f"自动替换失败: {e}")
            return False
    else:
        print("\n✗ 没有文件转换成功，请检查输入数据格式")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)