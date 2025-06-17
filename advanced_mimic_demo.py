#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级翻译对模仿演示程序
提供更直观的界面和更多功能选项
"""

import json
import os
import re
import random
from datetime import datetime
from typing import Dict, List, Any

class AdvancedTranslationMimic:
    def __init__(self):
        self.pairs_directory = "individual_pairs"
        self.translation_pairs = []
        self.patterns = self.load_patterns()
        self.load_data()
    
    def load_patterns(self):
        """加载翻译模式"""
        return {
            'pokemon_names': {
                'Garchomp': '烈咬陆鲨', 'Giratina-O': '骑拉帝纳-起源', 'Dondozo': '吃吼霸',
                'Mega Latias': '超级拉帝亚斯', 'Mega Scizor': '超级巨钳螳螂', 'Ferrothorn': '坚果哑铃',
                'Corviknight': '钢铠鸦', 'Tapu Lele': '卡璞·蝶蝶', 'Iron Valiant': '铁武者',
                'Weavile': '玛狃拉', 'Heatran': '席多蓝恩', 'Toxapex': '超坏星',
                'Gliscor': '天蝎王', 'Ting-Lu': '古鼎鹿', 'Volcarona': '火神蛾',
                'Raging Bolt': '猛雷鼓', 'Urshifu-R': '武道熊师-连击流', 'Landorus-T': '土地云-灵兽',
                'Rotom-W': '清洗洛托姆', 'Alomomola': '保姆曼波', 'Galarian Slowking': '伽勒尔呆呆王',
                'Ogerpon-W': '厄诡椪-水井面具', 'Mega Tyranitar': '超级班基拉斯', 'Zamazenta': '藏玛然特',
                'Clefable': '皮可西', 'Kartana': '纸御剑', 'Rillaboom': '轰擂金刚猩',
                'Ho-Oh': '凤王', 'Arceus-Fairy': '阿尔宙斯-妖精', 'Arceus-Water': '阿尔宙斯-水'
            },
            'moves': {
                'Shadow Ball': '影子球', 'Hex': '祸不单行', 'Calm Mind': '冥想',
                'Will-O-Wisp': '磷火', 'Stone Edge': '尖石攻击', 'Thunder Wave': '电磁波',
                'Poltergeist': '灵骚', 'Ruination': '大灾难', 'Dragon Dance': '龙之舞',
                'Liquidation': '水流裂破', 'Waterfall': '攀瀑', 'Curse': '诅咒',
                'Body Press': '扑击', 'Scale Shot': '鳞射', 'Fire Fang': '火焰牙',
                'Psychic': '精神强念', 'Psyshock': '精神冲击', 'Aura Sphere': '波导弹',
                'Ice Beam': '冰冻光束', 'Draco Meteor': '流星群', 'Spikes': '撒菱',
                'Stealth Rock': '隐形岩', 'Toxic': '剧毒', 'Substitute': '替身'
            },
            'abilities': {
                'Unaware': '纯朴', 'Levitate': '飘浮', 'Intimidate': '威吓'
            },
            'items': {
                'Heavy-Duty Boots': '厚底靴', 'Leftovers': '吃剩的东西',
                'Loaded Dice': '机变骰子', 'Choice Scarf': '讲究围巾'
            },
            'types': {
                'Dragon': '龙', 'Steel': '钢', 'Fire': '火', 'Water': '水',
                'Grass': '草', 'Electric': '电', 'Psychic': '超能力', 'Fighting': '格斗',
                'Poison': '毒', 'Ground': '地面', 'Flying': '飞行', 'Bug': '虫',
                'Rock': '岩石', 'Ghost': '幽灵', 'Ice': '冰', 'Dark': '恶', 'Fairy': '妖精'
            },
            'phrases': {
                'setup sweeper': '清场手', 'physical bulk': '物理耐久',
                'win condition': '获胜点', 'entry hazards': '钉子',
                'priority moves': '先制招式', 'offensive pressure': '进攻压力',
                'defensive typing': '防御属性', 'utility Pokemon': '功能型宝可梦',
                'bulky teams': '耐久向队伍', 'hyper offense': 'ho队伍',
                'dual screens': '双墙', 'STAB boost': '属性一致加成',
                'immune to': '免疫', 'super effective': '效果拔群',
                'not very effective': '效果不佳', 'chip damage': '消耗',
                'set up': '强化', 'sweep': '清场', 'recovery': '回复',
                'pivot': '中转', 'hazard removal': '清钉'
            }
        }
    
    def load_data(self):
        """加载翻译对数据"""
        if not os.path.exists(self.pairs_directory):
            print(f"❌ 目录 {self.pairs_directory} 不存在")
            return
        
        for filename in os.listdir(self.pairs_directory):
            if filename.endswith('.json'):
                filepath = os.path.join(self.pairs_directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'english' in data and 'chinese' in data:
                            self.translation_pairs.append(data)
                except Exception as e:
                    continue
        
        print(f"✅ 成功加载 {len(self.translation_pairs)} 个翻译对")
    
    def translate_text(self, text: str) -> str:
        """翻译文本"""
        result = text
        
        # 应用各种翻译模式
        for category, patterns in self.patterns.items():
            for en_term, cn_term in patterns.items():
                # 使用正则表达式进行精确匹配
                pattern = r'\b' + re.escape(en_term) + r'\b'
                result = re.sub(pattern, cn_term, result, flags=re.IGNORECASE)
        
        return result
    
    def analyze_translation(self, english: str, chinese: str) -> Dict[str, float]:
        """分析翻译质量"""
        # 计算覆盖率
        words = english.split()
        translated_count = 0
        
        for word in words:
            clean_word = re.sub(r'[^a-zA-Z-]', '', word)
            if any(clean_word.lower() in term.lower() 
                   for patterns in self.patterns.values() 
                   for term in patterns.keys()):
                translated_count += 1
        
        coverage = translated_count / len(words) if words else 0
        
        # 计算中文字符比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', chinese))
        total_chars = len(chinese)
        chinese_ratio = chinese_chars / total_chars if total_chars > 0 else 0
        
        # 计算完整度
        length_ratio = len(chinese) / len(english) if english else 0
        completeness = min(length_ratio, 1.0)
        
        return {
            'coverage': coverage,
            'chinese_ratio': chinese_ratio,
            'completeness': completeness,
            'overall_quality': (coverage + chinese_ratio + completeness) / 3
        }
    
    def generate_mimic_pair(self, base_text: str = None) -> Dict[str, Any]:
        """生成模仿翻译对"""
        if base_text is None:
            base_pair = random.choice(self.translation_pairs)
            base_text = base_pair['english']
        
        translated = self.translate_text(base_text)
        quality = self.analyze_translation(base_text, translated)
        
        return {
            'english': base_text,
            'chinese': translated,
            'quality': quality,
            'timestamp': datetime.now().isoformat()
        }
    
    def create_variation(self, text: str) -> str:
        """创建文本变体"""
        # 随机替换一些宝可梦名称
        pokemon_names = list(self.patterns['pokemon_names'].keys())
        
        for _ in range(2):  # 最多替换2次
            if len(pokemon_names) >= 2:
                old_name = random.choice(pokemon_names)
                new_name = random.choice(pokemon_names)
                if old_name != new_name and old_name in text:
                    text = text.replace(old_name, new_name, 1)
        
        return text
    
    def interactive_demo(self):
        """交互式演示"""
        print("\n" + "="*60)
        print("🎯 高级翻译对模仿演示程序")
        print("="*60)
        
        if not self.translation_pairs:
            print("❌ 没有可用的翻译对数据")
            return
        
        while True:
            print("\n📋 可用功能:")
            print("1️⃣  随机生成翻译对")
            print("2️⃣  自定义文本翻译")
            print("3️⃣  生成文本变体")
            print("4️⃣  查看统计信息")
            print("5️⃣  批量生成并保存")
            print("6️⃣  退出程序")
            
            try:
                choice = input("\n请选择功能 (1-6): ").strip()
                
                if choice == '1':
                    self.demo_random_generation()
                elif choice == '2':
                    self.demo_custom_translation()
                elif choice == '3':
                    self.demo_text_variation()
                elif choice == '4':
                    self.demo_statistics()
                elif choice == '5':
                    self.demo_batch_generation()
                elif choice == '6':
                    print("\n👋 感谢使用，再见！")
                    break
                else:
                    print("❌ 无效选择，请重试")
            
            except KeyboardInterrupt:
                print("\n\n👋 程序被中断，再见！")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")
    
    def demo_random_generation(self):
        """演示随机生成"""
        print("\n🎲 随机生成翻译对...")
        
        pair = self.generate_mimic_pair()
        
        print("\n📝 原文:")
        print(f"   {pair['english'][:200]}..." if len(pair['english']) > 200 else f"   {pair['english']}")
        
        print("\n🔄 译文:")
        print(f"   {pair['chinese'][:200]}..." if len(pair['chinese']) > 200 else f"   {pair['chinese']}")
        
        quality = pair['quality']
        print("\n📊 质量评估:")
        print(f"   覆盖率: {quality['coverage']:.1%}")
        print(f"   中文比例: {quality['chinese_ratio']:.1%}")
        print(f"   完整度: {quality['completeness']:.1%}")
        print(f"   总体质量: {quality['overall_quality']:.1%}")
    
    def demo_custom_translation(self):
        """演示自定义翻译"""
        print("\n✏️  自定义文本翻译")
        text = input("请输入要翻译的英文文本: ").strip()
        
        if not text:
            print("❌ 文本不能为空")
            return
        
        pair = self.generate_mimic_pair(text)
        
        print("\n📝 原文:")
        print(f"   {text}")
        
        print("\n🔄 译文:")
        print(f"   {pair['chinese']}")
        
        quality = pair['quality']
        print("\n📊 质量评估:")
        print(f"   覆盖率: {quality['coverage']:.1%}")
        print(f"   中文比例: {quality['chinese_ratio']:.1%}")
        print(f"   完整度: {quality['completeness']:.1%}")
        print(f"   总体质量: {quality['overall_quality']:.1%}")
    
    def demo_text_variation(self):
        """演示文本变体生成"""
        print("\n🔀 文本变体生成")
        
        # 选择一个基础文本
        base_pair = random.choice(self.translation_pairs)
        base_text = base_pair['english'][:300]  # 限制长度
        
        print("\n📝 基础文本:")
        print(f"   {base_text}...")
        
        # 生成3个变体
        print("\n🔄 生成的变体:")
        for i in range(3):
            variation = self.create_variation(base_text)
            translated = self.translate_text(variation)
            
            print(f"\n--- 变体 {i+1} ---")
            print(f"英文: {variation[:150]}...")
            print(f"中文: {translated[:150]}...")
    
    def demo_statistics(self):
        """演示统计信息"""
        print("\n📈 统计信息")
        print(f"\n📚 数据概览:")
        print(f"   翻译对总数: {len(self.translation_pairs)}")
        
        print(f"\n🎯 翻译模式统计:")
        for category, patterns in self.patterns.items():
            print(f"   {category}: {len(patterns)} 个模式")
        
        # 分析现有翻译对的质量
        if self.translation_pairs:
            print(f"\n🔍 质量分析 (前5个翻译对):")
            for i, pair in enumerate(self.translation_pairs[:5], 1):
                quality = self.analyze_translation(pair['english'], pair['chinese'])
                print(f"   翻译对 {i}: 总体质量 {quality['overall_quality']:.1%}")
    
    def demo_batch_generation(self):
        """演示批量生成"""
        print("\n📦 批量生成翻译对")
        
        try:
            count = int(input("请输入要生成的数量 (1-20): ").strip())
            if not 1 <= count <= 20:
                print("❌ 数量必须在1-20之间")
                return
        except ValueError:
            print("❌ 请输入有效数字")
            return
        
        print(f"\n🔄 正在生成 {count} 个翻译对...")
        
        generated_pairs = []
        for i in range(count):
            pair = self.generate_mimic_pair()
            generated_pairs.append(pair)
            print(f"   进度: {i+1}/{count}")
        
        # 计算平均质量
        avg_quality = sum(p['quality']['overall_quality'] for p in generated_pairs) / len(generated_pairs)
        
        print(f"\n✅ 生成完成！平均质量: {avg_quality:.1%}")
        
        # 保存选项
        save = input("\n💾 是否保存到文件? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"batch_generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            report = {
                'generation_date': datetime.now().isoformat(),
                'total_pairs': len(generated_pairs),
                'average_quality': avg_quality,
                'pairs': generated_pairs
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 已保存到: {filename}")

def main():
    """主函数"""
    print("🚀 启动高级翻译对模仿演示程序...")
    
    mimic = AdvancedTranslationMimic()
    mimic.interactive_demo()

if __name__ == "__main__":
    main()