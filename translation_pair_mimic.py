#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译对模仿程序
基于现有翻译对数据，学习翻译模式并生成新的翻译对
"""

import json
import os
import re
import random
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Tuple, Any

class TranslationPairMimic:
    def __init__(self, pairs_directory: str = "individual_pairs"):
        self.pairs_directory = pairs_directory
        self.translation_pairs = []
        self.patterns = {
            'pokemon_names': defaultdict(str),
            'move_names': defaultdict(str),
            'ability_names': defaultdict(str),
            'item_names': defaultdict(str),
            'type_names': defaultdict(str),
            'common_phrases': defaultdict(str),
            'sentence_structures': [],
            'translation_rules': []
        }
        self.load_translation_pairs()
        self.analyze_patterns()
    
    def load_translation_pairs(self):
        """加载所有翻译对数据"""
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
                except Exception as e:
                    print(f"加载文件 {filename} 时出错: {e}")
        
        print(f"成功加载 {len(self.translation_pairs)} 个翻译对")
    
    def analyze_patterns(self):
        """分析翻译模式"""
        print("正在分析翻译模式...")
        
        # 宝可梦名称模式
        pokemon_patterns = {
            'Garchomp': '烈咬陆鲨',
            'Giratina-O': '骑拉帝纳-起源',
            'Dondozo': '吃吼霸',
            'Mega Latias': '超级拉帝亚斯',
            'Mega Scizor': '超级巨钳螳螂',
            'Ferrothorn': '坚果哑铃',
            'Corviknight': '钢铠鸦',
            'Tapu Lele': '卡璞·蝶蝶',
            'Iron Valiant': '铁武者',
            'Weavile': '玛狃拉',
            'Heatran': '席多蓝恩',
            'Toxapex': '超坏星',
            'Gliscor': '天蝎王',
            'Ting-Lu': '古鼎鹿',
            'Volcarona': '火神蛾',
            'Raging Bolt': '猛雷鼓',
            'Urshifu-R': '武道熊师-连击流',
            'Landorus-T': '土地云-灵兽',
            'Rotom-W': '清洗洛托姆',
            'Alomomola': '保姆曼波',
            'Galarian Slowking': '伽勒尔呆呆王',
            'Ogerpon-W': '厄诡椪-水井面具',
            'Mega Tyranitar': '超级班基拉斯',
            'Zamazenta': '藏玛然特',
            'Clefable': '皮可西',
            'Kartana': '纸御剑',
            'Rillaboom': '轰擂金刚猩',
            'Ho-Oh': '凤王',
            'Arceus-Fairy': '阿尔宙斯-妖精',
            'Arceus-Water': '阿尔宙斯-水',
            'Arceus-Ground': '阿尔宙斯-地面'
        }
        
        # 招式名称模式
        move_patterns = {
            'Shadow Ball': '影子球',
            'Hex': '祸不单行',
            'Calm Mind': '冥想',
            'Will-O-Wisp': '磷火',
            'Stone Edge': '尖石攻击',
            'Thunder Wave': '电磁波',
            'Poltergeist': '灵骚',
            'Ruination': '大灾难',
            'Dragon Dance': '龙之舞',
            'Liquidation': '水流裂破',
            'Waterfall': '攀瀑',
            'Curse': '诅咒',
            'Body Press': '扑击',
            'Scale Shot': '鳞射',
            'Fire Fang': '火焰牙',
            'Psychic': '精神强念',
            'Psyshock': '精神冲击',
            'Aura Sphere': '波导弹',
            'Ice Beam': '冰冻光束',
            'Draco Meteor': '流星群',
            'Spikes': '撒菱',
            'Stealth Rock': '隐形岩',
            'Toxic': '剧毒',
            'Substitute': '替身',
            'Stored Power': '辅助力量'
        }
        
        # 特性名称模式
        ability_patterns = {
            'Unaware': '纯朴',
            'Levitate': '飘浮'
        }
        
        # 道具名称模式
        item_patterns = {
            'Heavy-Duty Boots': '厚底靴',
            'Leftovers': '吃剩的东西',
            'Loaded Dice': '机变骰子',
            'Latiasite': 'Latiasite'
        }
        
        # 属性名称模式
        type_patterns = {
            'Dragon': '龙',
            'Steel': '钢',
            'Fire': '火',
            'Water': '水',
            'Grass': '草',
            'Electric': '电',
            'Psychic': '超能力',
            'Fighting': '格斗',
            'Poison': '毒',
            'Ground': '地面',
            'Flying': '飞行',
            'Bug': '虫',
            'Rock': '岩石',
            'Ghost': '幽灵',
            'Ice': '冰',
            'Dark': '恶',
            'Fairy': '妖精'
        }
        
        # 常用短语模式
        phrase_patterns = {
            'setup sweeper': '清场手',
            'physical bulk': '物理耐久',
            'special bulk': '特殊耐久',
            'win condition': '获胜点',
            'entry hazards': '钉子',
            'priority moves': '先制招式',
            'checks and counters': 'check和counter',
            'offensive pressure': '进攻压力',
            'defensive typing': '防御属性',
            'utility Pokemon': '功能型宝可梦',
            'bulky teams': '耐久向队伍',
            'hyper offense': 'ho队伍',
            'dual screens': '双墙',
            'status moves': '变化招式',
            'STAB boost': '属性一致加成',
            'Tera type': '太晶属性',
            'Terastallized': '太晶化',
            'immune to': '免疫',
            'resistant to': '抵抗',
            'weak to': '弱点是',
            'super effective': '效果拔群',
            'not very effective': '效果不佳',
            'chip damage': '消耗',
            'passive nature': '被动',
            'offensive threats': '进攻威胁',
            'defensive wall': '盾牌',
            'pivot': '中转',
            'hazard removal': '清钉',
            'recovery': '回复',
            'set up': '强化',
            'sweep': '清场',
            'OHKO': 'OHKO',
            '2HKO': '2HKO'
        }
        
        # 更新模式字典
        self.patterns['pokemon_names'].update(pokemon_patterns)
        self.patterns['move_names'].update(move_patterns)
        self.patterns['ability_names'].update(ability_patterns)
        self.patterns['item_names'].update(item_patterns)
        self.patterns['type_names'].update(type_patterns)
        self.patterns['common_phrases'].update(phrase_patterns)
        
        # 分析句子结构
        self.analyze_sentence_structures()
        
        print(f"分析完成:")
        print(f"- 宝可梦名称: {len(self.patterns['pokemon_names'])}")
        print(f"- 招式名称: {len(self.patterns['move_names'])}")
        print(f"- 特性名称: {len(self.patterns['ability_names'])}")
        print(f"- 道具名称: {len(self.patterns['item_names'])}")
        print(f"- 属性名称: {len(self.patterns['type_names'])}")
        print(f"- 常用短语: {len(self.patterns['common_phrases'])}")
    
    def analyze_sentence_structures(self):
        """分析句子结构模式"""
        structures = [
            {
                'english_pattern': r'(\w+) is a (\w+) (.+) that (.+)',
                'chinese_template': '{0}是一个{1}的{2}，{3}',
                'description': '基本描述模式'
            },
            {
                'english_pattern': r'(\w+) uses (.+) to (.+)',
                'chinese_template': '{0}使用{1}来{2}',
                'description': '使用模式'
            },
            {
                'english_pattern': r'(\w+) can (.+) against (.+)',
                'chinese_template': '{0}可以对{2}{1}',
                'description': '对抗模式'
            },
            {
                'english_pattern': r'(\w+) struggles against (.+)',
                'chinese_template': '{0}难以对抗{1}',
                'description': '困难模式'
            },
            {
                'english_pattern': r'(\w+) appreciates (.+)',
                'chinese_template': '{0}欣赏{1}',
                'description': '欣赏模式'
            }
        ]
        
        self.patterns['sentence_structures'] = structures
    
    def translate_text(self, english_text: str) -> str:
        """基于学习的模式翻译文本"""
        chinese_text = english_text
        
        # 应用宝可梦名称翻译
        for en_name, cn_name in self.patterns['pokemon_names'].items():
            chinese_text = re.sub(r'\b' + re.escape(en_name) + r'\b', cn_name, chinese_text)
        
        # 应用招式名称翻译
        for en_move, cn_move in self.patterns['move_names'].items():
            chinese_text = re.sub(r'\b' + re.escape(en_move) + r'\b', cn_move, chinese_text)
        
        # 应用特性名称翻译
        for en_ability, cn_ability in self.patterns['ability_names'].items():
            chinese_text = re.sub(r'\b' + re.escape(en_ability) + r'\b', cn_ability, chinese_text)
        
        # 应用道具名称翻译
        for en_item, cn_item in self.patterns['item_names'].items():
            chinese_text = re.sub(r'\b' + re.escape(en_item) + r'\b', cn_item, chinese_text)
        
        # 应用属性名称翻译
        for en_type, cn_type in self.patterns['type_names'].items():
            chinese_text = re.sub(r'\b' + re.escape(en_type) + r'\b', cn_type, chinese_text)
        
        # 应用常用短语翻译
        for en_phrase, cn_phrase in self.patterns['common_phrases'].items():
            chinese_text = re.sub(re.escape(en_phrase), cn_phrase, chinese_text, flags=re.IGNORECASE)
        
        return chinese_text
    
    def generate_mimic_pair(self, base_pair: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成模仿的翻译对"""
        if base_pair is None:
            base_pair = random.choice(self.translation_pairs)
        
        # 创建新的翻译对
        new_pair = {
            'id': f'mimic_{len(self.translation_pairs) + 1}',
            'english': base_pair['english'],
            'chinese': self.translate_text(base_pair['english']),
            'section_type': base_pair.get('section_type', 'GENERATED'),
            'source_file': f"mimic_generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            'confidence': 0.8,
            'generation_method': 'pattern_based_mimic',
            'base_pair_id': base_pair.get('id', 'unknown')
        }
        
        return new_pair
    
    def generate_template_variations(self, template_text: str, variations: int = 3) -> List[Dict[str, Any]]:
        """基于模板生成变体"""
        results = []
        
        # 获取模板中的关键词
        pokemon_names = list(self.patterns['pokemon_names'].keys())
        move_names = list(self.patterns['move_names'].keys())
        
        for i in range(variations):
            # 随机替换宝可梦名称
            modified_text = template_text
            for _ in range(2):  # 最多替换2个宝可梦
                old_pokemon = random.choice(pokemon_names)
                new_pokemon = random.choice(pokemon_names)
                if old_pokemon != new_pokemon:
                    modified_text = modified_text.replace(old_pokemon, new_pokemon, 1)
            
            # 随机替换招式名称
            for _ in range(1):  # 最多替换1个招式
                old_move = random.choice(move_names)
                new_move = random.choice(move_names)
                if old_move != new_move:
                    modified_text = modified_text.replace(old_move, new_move, 1)
            
            # 生成翻译对
            pair = {
                'id': f'template_variation_{i+1}',
                'english': modified_text,
                'chinese': self.translate_text(modified_text),
                'section_type': 'TEMPLATE_VARIATION',
                'source_file': f"template_variation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                'confidence': 0.7,
                'generation_method': 'template_variation'
            }
            
            results.append(pair)
        
        return results
    
    def evaluate_translation_quality(self, pair: Dict[str, Any]) -> Dict[str, float]:
        """评估翻译质量"""
        english_text = pair['english']
        chinese_text = pair['chinese']
        
        # 计算覆盖率
        total_words = len(english_text.split())
        translated_words = 0
        
        for word in english_text.split():
            word_clean = re.sub(r'[^a-zA-Z-]', '', word)
            if any(word_clean.lower() in pattern.lower() for patterns in self.patterns.values() 
                   if isinstance(patterns, dict) for pattern in patterns.keys()):
                translated_words += 1
        
        coverage = translated_words / total_words if total_words > 0 else 0
        
        # 计算中文比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', chinese_text))
        total_chars = len(chinese_text)
        chinese_ratio = chinese_chars / total_chars if total_chars > 0 else 0
        
        # 计算完整度（基于长度比例）
        length_ratio = len(chinese_text) / len(english_text) if len(english_text) > 0 else 0
        completeness = min(length_ratio, 1.0)
        
        return {
            'coverage': coverage,
            'chinese_ratio': chinese_ratio,
            'completeness': completeness,
            'overall_quality': (coverage + chinese_ratio + completeness) / 3
        }
    
    def batch_generate_pairs(self, count: int = 10) -> List[Dict[str, Any]]:
        """批量生成翻译对"""
        generated_pairs = []
        
        for i in range(count):
            # 随机选择基础翻译对
            base_pair = random.choice(self.translation_pairs)
            
            # 生成模仿翻译对
            mimic_pair = self.generate_mimic_pair(base_pair)
            
            # 评估质量
            quality = self.evaluate_translation_quality(mimic_pair)
            mimic_pair['quality_metrics'] = quality
            
            generated_pairs.append(mimic_pair)
        
        return generated_pairs
    
    def save_generated_pairs(self, pairs: List[Dict[str, Any]], filename: str = None):
        """保存生成的翻译对"""
        if filename is None:
            filename = f"generated_translation_pairs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # 创建报告
        report = {
            'generation_date': datetime.now().isoformat(),
            'total_pairs': len(pairs),
            'generation_method': 'pattern_based_mimic',
            'source_patterns': {
                'pokemon_names': len(self.patterns['pokemon_names']),
                'move_names': len(self.patterns['move_names']),
                'ability_names': len(self.patterns['ability_names']),
                'item_names': len(self.patterns['item_names']),
                'type_names': len(self.patterns['type_names']),
                'common_phrases': len(self.patterns['common_phrases'])
            },
            'quality_summary': self.calculate_quality_summary(pairs),
            'generated_pairs': pairs
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"生成的翻译对已保存到: {filename}")
    
    def calculate_quality_summary(self, pairs: List[Dict[str, Any]]) -> Dict[str, float]:
        """计算质量摘要"""
        if not pairs:
            return {}
        
        metrics = ['coverage', 'chinese_ratio', 'completeness', 'overall_quality']
        summary = {}
        
        for metric in metrics:
            values = [pair.get('quality_metrics', {}).get(metric, 0) for pair in pairs]
            summary[f'avg_{metric}'] = sum(values) / len(values) if values else 0
            summary[f'min_{metric}'] = min(values) if values else 0
            summary[f'max_{metric}'] = max(values) if values else 0
        
        return summary
    
    def interactive_demo(self):
        """交互式演示"""
        print("\n=== 翻译对模仿程序交互式演示 ===")
        print("可用命令:")
        print("1. generate [数量] - 生成指定数量的翻译对")
        print("2. translate [英文文本] - 翻译指定文本")
        print("3. analyze - 显示分析统计")
        print("4. template [模板文本] - 基于模板生成变体")
        print("5. save [文件名] - 保存最近生成的翻译对")
        print("6. quit - 退出")
        
        recent_pairs = []
        
        while True:
            try:
                command = input("\n请输入命令: ").strip()
                
                if command.startswith('generate'):
                    parts = command.split()
                    count = int(parts[1]) if len(parts) > 1 else 5
                    print(f"正在生成 {count} 个翻译对...")
                    pairs = self.batch_generate_pairs(count)
                    recent_pairs = pairs
                    
                    for i, pair in enumerate(pairs[:3], 1):  # 显示前3个
                        print(f"\n--- 翻译对 {i} ---")
                        print(f"英文: {pair['english'][:200]}...")
                        print(f"中文: {pair['chinese'][:200]}...")
                        quality = pair['quality_metrics']
                        print(f"质量: 覆盖率={quality['coverage']:.2f}, 中文比例={quality['chinese_ratio']:.2f}, 完整度={quality['completeness']:.2f}")
                
                elif command.startswith('translate'):
                    text = command[9:].strip()
                    if text:
                        result = self.translate_text(text)
                        print(f"\n原文: {text}")
                        print(f"译文: {result}")
                    else:
                        print("请提供要翻译的文本")
                
                elif command == 'analyze':
                    print(f"\n=== 分析统计 ===")
                    print(f"加载的翻译对数量: {len(self.translation_pairs)}")
                    print(f"宝可梦名称模式: {len(self.patterns['pokemon_names'])}")
                    print(f"招式名称模式: {len(self.patterns['move_names'])}")
                    print(f"特性名称模式: {len(self.patterns['ability_names'])}")
                    print(f"道具名称模式: {len(self.patterns['item_names'])}")
                    print(f"属性名称模式: {len(self.patterns['type_names'])}")
                    print(f"常用短语模式: {len(self.patterns['common_phrases'])}")
                
                elif command.startswith('template'):
                    template = command[8:].strip()
                    if template:
                        variations = self.generate_template_variations(template, 3)
                        recent_pairs = variations
                        print(f"\n基于模板生成了 {len(variations)} 个变体:")
                        for i, var in enumerate(variations, 1):
                            print(f"\n--- 变体 {i} ---")
                            print(f"英文: {var['english'][:150]}...")
                            print(f"中文: {var['chinese'][:150]}...")
                    else:
                        print("请提供模板文本")
                
                elif command.startswith('save'):
                    parts = command.split()
                    filename = parts[1] if len(parts) > 1 else None
                    if recent_pairs:
                        self.save_generated_pairs(recent_pairs, filename)
                    else:
                        print("没有可保存的翻译对，请先生成一些翻译对")
                
                elif command == 'quit':
                    print("再见！")
                    break
                
                else:
                    print("未知命令，请重试")
            
            except KeyboardInterrupt:
                print("\n程序被中断")
                break
            except Exception as e:
                print(f"发生错误: {e}")

def main():
    """主函数"""
    print("翻译对模仿程序启动中...")
    
    # 创建模仿器实例
    mimic = TranslationPairMimic()
    
    if not mimic.translation_pairs:
        print("未找到翻译对数据，程序退出")
        return
    
    # 生成示例翻译对
    print("\n=== 生成示例翻译对 ===")
    sample_pairs = mimic.batch_generate_pairs(5)
    
    for i, pair in enumerate(sample_pairs, 1):
        print(f"\n--- 示例 {i} ---")
        print(f"ID: {pair['id']}")
        print(f"英文: {pair['english'][:150]}...")
        print(f"中文: {pair['chinese'][:150]}...")
        quality = pair['quality_metrics']
        print(f"质量评分: {quality['overall_quality']:.2f}")
    
    # 保存示例结果
    mimic.save_generated_pairs(sample_pairs, "sample_mimic_pairs.json")
    
    # 启动交互式演示
    mimic.interactive_demo()

if __name__ == "__main__":
    main()