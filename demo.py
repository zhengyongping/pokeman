#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英译中个性化翻译程序演示脚本
展示程序的各种功能
"""

import subprocess
import time

def run_command(cmd):
    """运行命令并显示结果"""
    print(f"\n>>> {cmd}")
    print("-" * 50)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"错误: {result.stderr}")
    print("-" * 50)
    time.sleep(1)

def main():
    print("=" * 60)
    print("英译中个性化翻译程序演示")
    print("=" * 60)
    
    # 1. 显示帮助信息
    print("\n1. 显示程序帮助信息")
    run_command('python3 translator.py --help')
    
    # 2. 基础翻译测试
    print("\n2. 基础翻译功能测试")
    test_sentences = [
        "Hello world",
        "Good morning",
        "Thank you",
        "The pokemon trainer caught a legendary pokemon",
        "Pokemon battle is exciting"
    ]
    
    for sentence in test_sentences:
        run_command(f'python3 translator.py --translate "{sentence}"')
    
    # 3. 显示初始学习进度
    print("\n3. 显示初始学习进度")
    run_command('python3 translator.py --progress')
    
    print("\n=" * 60)
    print("演示完成！")
    print("\n接下来你可以尝试:")
    print("1. 使用 --interactive 模式进行交互式翻译")
    print("2. 使用 --learn 模式添加学习样本")
    print("3. 添加样本后再次测试翻译效果")
    print("=" * 60)

if __name__ == "__main__":
    main()