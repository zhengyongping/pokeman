#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import Optional

def _clean_chinese_set_comments(text: str) -> str:
    """清理中文SET COMMENTS，移除Chinese Set配置信息"""
    # 移除Chinese Set配置行
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        # 跳过Chinese Set配置行（包含||分隔符的完整配置行）
        if (line.startswith('Chinese set:') or line.startswith('Chinese Set:') or 
            line.startswith('Chinese set：') or line.startswith('Chinese Set：')):
            continue
        # 跳过包含||分隔符的配置行（这通常是宝可梦配置信息）
        if '||' in line and ('道具：' in line or '特性：' in line or '努力值：' in line or '性格：' in line or '招式：' in line):
            continue
        if line:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines).strip()

def test_cleaning():
    # 测试数据
    test_text = """Chinese set：突击背心洗翠大剑鬼||道具：突击背心||特性：锋锐||努力值：168HP/176攻击/80特防/84速度||性格：固执||招式：贝壳刃|秘剑•千重涛|突袭|拍落/快速折返/圣剑
除了通常的功能性，洗翠大剑鬼携带突击背心带来的额外耐久使其能更好地check赛富豪，并有机会对超级蒂安希等宝可梦造成意外击杀。拍落可以移除保姆曼波和超坏星的厚底靴以及坚果哑铃的吃剩的东西，从而增强其设置的撒菱的伤害。也可选择快速折返来帮助队伍赚取节奏，或使用圣剑来OHKO仆刀将军。给定的努力值分配让洗翠大剑鬼能在满HP下承受超级蒂安希的月亮之力或超级喷火龙Y的日光束，同时速度超过未分配速度努力值的天蝎王。
突击背心洗翠大剑鬼最适合搭配青睐其功能性与定位的平衡攻队。由于速度偏慢，它容易被藏玛然特、卡璞·蝶蝶等高速宝可梦复仇杀，因此需要土地云-灵兽、赛富豪等防御型队友联防这些威胁。其中赛富豪不仅能抵挡格斗与妖精属性招式，还能封锁对方全类型的扫钉手段。能设置隐形岩的队友如雄伟牙和土地云-灵兽同样重要，它们能进一步积累场地伤害，同时从洗翠大剑鬼移除超坏星和保姆曼波等宝可梦的道具中受益。而像超级蒂安希、铁武者和藏玛然特等妖精或格斗属性宝可梦则青睐洗翠大剑鬼的撒钉能力与对赛富豪的压制力，帮助削弱坚果哑铃和赛富豪等check；作为回报，它们能解决大剑鬼难以应对的轰鸣月等恶属性与敌方藏玛然特等格斗属性威胁。"""
    
    print("原始文本:")
    print(test_text)
    print("\n" + "="*50 + "\n")
    
    cleaned = _clean_chinese_set_comments(test_text)
    print("清理后文本:")
    print(cleaned)
    
    # 检查是否还包含配置信息
    if 'Chinese set：' in cleaned or '||' in cleaned:
        print("\n❌ 清理失败：仍包含配置信息")
    else:
        print("\n✅ 清理成功：配置信息已移除")

if __name__ == "__main__":
    test_cleaning()