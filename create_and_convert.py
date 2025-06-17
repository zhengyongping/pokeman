#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建示例数据并转换格式的一体化脚本
"""

import os
import json
import shutil
import time

def create_sample_data():
    """创建示例翻译对数据"""
    print("创建示例翻译对数据...")
    
    # 确保目录存在
    os.makedirs("individual_pairs", exist_ok=True)
    
    # 示例数据
    samples = [
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
                },
                {
                    "english": "Nice to meet you.",
                    "chinese": "很高兴见到你。"
                }
            ]
        },
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
                },
                {
                    "english": "Gyarados is a Water and Flying type Pokemon.",
                    "chinese": "暴鲤龙是水系和飞行系宝可梦。"
                }
            ]
        },
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
                },
                {
                    "source": "Have a nice day!",
                    "target": "祝你今天愉快！"
                }
            ]
        }
    ]
    
    for sample in samples:
        file_path = os.path.join("individual_pairs", sample["filename"])
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sample["data"], f, ensure_ascii=False, indent=2)
        print(f"✓ 创建: {file_path}")
    
    print(f"成功创建 {len(samples)} 个示例文件")
    return True

def detect_language(text):
    """简单的语言检测"""
    import re
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.strip())
    
    if total_chars == 0:
        return "unknown"
    
    if chinese_chars / total_chars > 0.3:
        return "chinese"
    else:
        return "english"

def convert_item(item):
    """转换单个数据项"""
    source_fields = ['source', 'english', 'en', 'eng', 'original']
    target_fields = ['target', 'chinese', 'zh', 'chn', 'translation']
    
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
    
    return {
        "source": source_text,
        "target": target_text,
        "source_lang": detect_language(source_text),
        "target_lang": detect_language(target_text)
    }

def convert_file(input_file, output_file):
    """转换单个文件"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        converted_items = []
        
        if isinstance(data, dict):
            converted = convert_item(data)
            if converted:
                converted_items.append(converted)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    converted = convert_item(item)
                    if converted:
                        converted_items.append(converted)
        
        if converted_items:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(converted_items, f, ensure_ascii=False, indent=2)
            return len(converted_items)
        
        return 0
        
    except Exception as e:
        print(f"转换文件 {input_file} 时出错: {e}")
        return 0

def convert_all_files():
    """转换所有文件"""
    print("\n转换数据格式...")
    
    input_dir = "individual_pairs"
    output_dir = "individual_pairs_formatted"
    
    # 获取所有JSON文件
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    
    if not json_files:
        print("没有找到JSON文件")
        return False
    
    total_pairs = 0
    success_files = 0
    
    for filename in json_files:
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename)
        
        pairs_count = convert_file(input_file, output_file)
        if pairs_count > 0:
            print(f"✓ {filename}: {pairs_count} 个翻译对")
            total_pairs += pairs_count
            success_files += 1
        else:
            print(f"✗ {filename}: 转换失败")
    
    print(f"\n转换完成: {success_files}/{len(json_files)} 个文件, 共 {total_pairs} 个翻译对")
    return success_files > 0

def replace_directory():
    """替换目录"""
    print("\n替换目录...")
    
    input_dir = "individual_pairs"
    output_dir = "individual_pairs_formatted"
    
    try:
        # 备份原目录
        backup_dir = f"{input_dir}_backup_{int(time.time())}"
        shutil.move(input_dir, backup_dir)
        print(f"✓ 原目录备份为: {backup_dir}")
        
        # 重命名输出目录
        shutil.move(output_dir, input_dir)
        print(f"✓ 格式化目录重命名为: {input_dir}")
        
        return True
        
    except Exception as e:
        print(f"替换目录失败: {e}")
        return False

def main():
    """主函数"""
    print("数据格式转换工具")
    print("=" * 50)
    
    # 步骤1: 创建示例数据
    if not create_sample_data():
        print("创建示例数据失败")
        return
    
    # 步骤2: 转换格式
    if not convert_all_files():
        print("格式转换失败")
        return
    
    # 步骤3: 替换目录
    if not replace_directory():
        print("目录替换失败")
        return
    
    print("\n" + "=" * 50)
    print("✓ 数据格式转换完成！")
    print("\n现在可以运行 NLLB 学习模块:")
    print("python run_nllb_learning.py")
    print("\n或者运行快速测试:")
    print("python quick_test.py")

if __name__ == "__main__":
    main()