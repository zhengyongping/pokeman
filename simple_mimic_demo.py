#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的翻译对模仿演示
展示核心功能和生成结果
"""

import json
import os
import re
import random
from datetime import datetime
from typing import Dict, List, Any

class SimpleMimicDemo:
    def __init__(self):
        self.pairs_directory = "individual_pairs"
        self.translation_pairs = []
        self.patterns = {
            'pokemon_names': {
                'Garchomp': '烈咬陆鲨', 'Giratina-O': '骑拉帝纳-起源', 'Dondozo': '吃吼霸',
                'Mega Latias': '超级拉帝亚斯', 'Mega Scizor': '超级巨钳螳螂', 'Ferrothorn': '坚果哑铃',
                'Corviknight': '钢铠鸦', 'Tapu Lele': '卡璞·蝶蝶', 'Iron Valiant': '铁武者',
                'Weavile': '玛狃拉', 'Heatran': '席多蓝恩', 'Toxapex': '超坏星',
                'Gliscor': '天蝎王', 'Ting-Lu': '古鼎鹿', 'Volcarona': '火神蛾',
                'Raging Bolt': '猛雷鼓', 'Urshifu-R': '武道熊师-连击流', 'Landorus-T': '土地云-灵兽',
                'Rotom-W': '清洗洛托姆', 'Alomomola': '保姆曼波', 'Galarian Slowking': '伽勒尔呆呆王',
                'Ogerpon-W': '厄诡椪-水井面具', 'Mega Tyranitar': '超级班基拉斯', 'Zamazenta': '藏玛然特',
                'Clefable': '皮可西', 'Kartana': '纸御剑', 'Rillaboom': '轰擂金刚猩'
            },
            'moves': {
                'Shadow Ball': '影子球', 'Hex': '祸不单行', 'Calm Mind': '冥想',
                'Will-O-Wisp': '磷火', 'Stone Edge': '尖石攻击', 'Thunder Wave': '电磁波',
                'Dragon Dance': '龙之舞', 'Scale Shot': '鳞射', 'Fire Fang': '火焰牙',
                'Psychic': '精神强念', 'Psyshock': '精神冲击', 'Aura Sphere': '波导弹',
                'Ice Beam': '冰冻光束', 'Stealth Rock': '隐形岩', 'Toxic': '剧毒'
            },
            'phrases': {
                'setup sweeper': '清场手', 'physical bulk': '物理耐久',
                'win condition': '获胜点', 'entry hazards': '钉子',
                'priority moves': '先制招式', 'offensive pressure': '进攻压力',
                'defensive typing': '防御属性', 'utility Pokemon': '功能型宝可梦',
                'immune to': '免疫', 'super effective': '效果拔群',
                'set up': '强化', 'sweep': '清场', 'recovery': '回复'
            }
        }
        self.load_data()
    
    def load_data(self):
        """加载翻译对数据"""
        if not os.path.exists(self.pairs_directory):
            print(f"目录 {self.pairs_directory} 不存在")
            return
        
        for filename in os.listdir(self.pairs_directory):
            if filename.endswith('.json'):
                filepath = os.path.join(self.pairs_directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'english' in data and 'chinese' in data:
                            self.translation_pairs.append(data)
                except:
                    continue
        
        print(f"成功加载 {len(self.translation_pairs)} 个翻译对")
    
    def translate_text(self, text: str) -> str:
        """翻译文本"""
        result = text
        
        # 应用翻译模式
        for category, patterns in self.patterns.items():
            for en_term, cn_term in patterns.items():
                pattern = r'\b' + re.escape(en_term) + r'\b'
                result = re.sub(pattern, cn_term, result, flags=re.IGNORECASE)
        
        return result
    
    def analyze_quality(self, english: str, chinese: str) -> Dict[str, float]:
        """分析翻译质量"""
        words = english.split()
        translated_count = 0
        
        for word in words:
            clean_word = re.sub(r'[^a-zA-Z-]', '', word)
            if any(clean_word.lower() in term.lower() 
                   for patterns in self.patterns.values() 
                   for term in patterns.keys()):
                translated_count += 1
        
        coverage = translated_count / len(words) if words else 0
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', chinese))
        chinese_ratio = chinese_chars / len(chinese) if chinese else 0
        
        return {
            'coverage': coverage,
            'chinese_ratio': chinese_ratio,
            'overall_quality': (coverage + chinese_ratio) / 2
        }
    
    def generate_demo_pairs(self, count: int = 3) -> List[Dict[str, Any]]:
        """生成演示翻译对"""
        results = []
        
        for i in range(count):
            # 随机选择基础翻译对
            base_pair = random.choice(self.translation_pairs)
            english_text = base_pair['english']
            
            # 生成翻译
            chinese_text = self.translate_text(english_text)
            
            # 分析质量
            quality = self.analyze_quality(english_text, chinese_text)
            
            result = {
                'id': f'demo_{i+1}',
                'english': english_text,
                'chinese': chinese_text,
                'quality': quality,
                'source_id': base_pair.get('id', 'unknown')
            }
            
            results.append(result)
        
        return results
    
    def create_variations(self, base_text: str, count: int = 2) -> List[str]:
        """创建文本变体"""
        variations = []
        pokemon_names = list(self.patterns['pokemon_names'].keys())
        
        for i in range(count):
            text = base_text
            
            # 随机替换宝可梦名称
            for _ in range(2):
                if len(pokemon_names) >= 2:
                    old_name = random.choice(pokemon_names)
                    new_name = random.choice(pokemon_names)
                    if old_name != new_name and old_name in text:
                        text = text.replace(old_name, new_name, 1)
            
            variations.append(text)
        
        return variations
    
    def run_demo(self):
        """运行演示"""
        print("\n" + "="*60)
        print("翻译对模仿演示程序")
        print("="*60)
        
        if not self.translation_pairs:
            print("没有可用的翻译对数据")
            return
        
        print(f"\n数据统计:")
        print(f"- 翻译对数量: {len(self.translation_pairs)}")
        print(f"- 宝可梦名称: {len(self.patterns['pokemon_names'])}")
        print(f"- 招式名称: {len(self.patterns['moves'])}")
        print(f"- 常用短语: {len(self.patterns['phrases'])}")
        
        # 生成演示翻译对
        print("\n" + "-"*60)
        print("生成演示翻译对")
        print("-"*60)
        
        demo_pairs = self.generate_demo_pairs(3)
        
        for i, pair in enumerate(demo_pairs, 1):
            print(f"\n=== 演示 {i} ===")
            print(f"原文: {pair['english'][:150]}...")
            print(f"译文: {pair['chinese'][:150]}...")
            quality = pair['quality']
            print(f"质量: 覆盖率={quality['coverage']:.1%}, 中文比例={quality['chinese_ratio']:.1%}, 总体={quality['overall_quality']:.1%}")
        
        # 生成文本变体
        print("\n" + "-"*60)
        print("生成文本变体")
        print("-"*60)
        
        base_text = "Garchomp is a setup sweeper that can use Dragon Dance to boost its Attack and Speed."
        print(f"\n基础文本: {base_text}")
        
        variations = self.create_variations(base_text, 2)
        for i, variation in enumerate(variations, 1):
            translated = self.translate_text(variation)
            print(f"\n变体 {i}:")
            print(f"英文: {variation}")
            print(f"中文: {translated}")
        
        # 保存结果
        print("\n" + "-"*60)
        print("保存演示结果")
        print("-"*60)
        
        report = {
            'demo_date': datetime.now().isoformat(),
            'total_pairs': len(demo_pairs),
            'average_quality': sum(p['quality']['overall_quality'] for p in demo_pairs) / len(demo_pairs),
            'demo_pairs': demo_pairs,
            'text_variations': {
                'base_text': base_text,
                'variations': [{
                    'english': var,
                    'chinese': self.translate_text(var)
                } for var in variations]
            }
        }
        
        filename = f"mimic_demo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"演示结果已保存到: {filename}")
        
        # 显示总结
        avg_quality = report['average_quality']
        print(f"\n总结:")
        print(f"- 生成了 {len(demo_pairs)} 个翻译对")
        print(f"- 平均质量: {avg_quality:.1%}")
        print(f"- 生成了 {len(variations)} 个文本变体")
        print(f"- 演示完成！")

def main():
    """主函数"""
    print("启动翻译对模仿演示...")
    
    demo = SimpleMimicDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()