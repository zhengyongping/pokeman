# -*- coding: utf-8 -*-
"""
改进版翻译器 - 支持更好的长文本翻译
"""

import json
import re
from typing import Dict, List, Tuple

class ImprovedTranslator:
    def __init__(self):
        self.dictionary = {}
        self.compound_terms = {}
        self.grammar_rules = {}
        self.load_translation_data()
        self.build_advanced_patterns()
    
    def load_translation_data(self):
        """加载翻译数据"""
        try:
            with open('enhanced_translation_results.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.dictionary = data.get('enhanced_dictionary', {})
            print(f"已加载 {len(self.dictionary)} 个术语")
        except:
            print("无法加载翻译数据")
    
    def build_advanced_patterns(self):
        """构建高级翻译模式"""
        # 复合术语（多词组合）
        self.compound_terms = {
            'swords dance': '剑舞',
            'dragon dance': '龙之舞',
            'calm mind': '冥想',
            'nasty plot': '诡计',
            'choice band': '讲究头带',
            'choice specs': '讲究眼镜',
            'choice scarf': '讲究围巾',
            'life orb': '生命宝珠',
            'assault vest': '突击背心',
            'stealth rock': '隐形岩',
            'magic guard': '魔法防守',
            'ice punch': '冰冻拳',
            'thunder punch': '雷电拳',
            'fire punch': '火焰拳',
            'close combat': '近身战',
            'volt switch': '伏特替换',
            'knock off': '拍落',
            'sucker punch': '突袭',
            'u-turn': 'U型回转',
            'tapu koko': '卡璞·鸣鸣',
            'special attack': '特攻',
            'special defense': '特防',
            'physical attack': '物攻',
            'physical defense': '物防',
            'hidden ability': '隐藏特性',
            'priority move': '先制招式',
            'status move': '变化招式',
            'revenge kill': '报仇击杀'
        }
        
        # 语法规则和句型转换
        self.grammar_rules = {
            # 基本句型
            r'(\w+)\s+is\s+a\s+(great|good|excellent|powerful)\s+(\w+)': r'\1是一个优秀的\3',
            r'(\w+)\s+can\s+be\s+used\s+as\s+a\s+(\w+)': r'\1可以用作\2',
            r'(\w+)\s+serves\s+as\s+(the\s+)?(\w+)': r'\1担任\3',
            r'(\w+)\s+acts\s+as\s+a\s+(\w+)': r'\1充当\2',
            r'(\w+)\s+works\s+well\s+with\s+(\w+)': r'\1与\2配合良好',
            r'(\w+)\s+provides\s+(\w+)': r'\1提供\2',
            r'(\w+)\s+gives\s+(\w+)\s+coverage': r'\1为\2提供打击面',
            
            # 战斗相关
            r'(\w+)\s+can\s+OHKO\s+(\w+)': r'\1可以一击击倒\2',
            r'(\w+)\s+can\s+2HKO\s+(\w+)': r'\1可以二击击倒\2',
            r'(\w+)\s+resists\s+(\w+)': r'\1抗性\2',
            r'(\w+)\s+is\s+weak\s+to\s+(\w+)': r'\1弱点是\2',
            r'(\w+)\s+is\s+immune\s+to\s+(\w+)': r'\1免疫\2',
            
            # 配置相关
            r'This\s+(\w+)\s+set\s+is\s+designed\s+to\s+(.+)': r'这个\1配置旨在\2',
            r'(\w+)\s+set': r'\1配置',
            r'(\w+)\s+build': r'\1构筑',
            r'(\w+)\s+team': r'\1队伍',
            
            # 道具相关
            r'(\w+)\s+with\s+(\w+)': r'携带\2的\1',
            r'(\w+)\s+holds\s+(\w+)': r'\1携带\2',
            
            # 特性相关
            r'(\w+)\s+has\s+(\w+)\s+ability': r'\1具有\2特性',
            r'(\w+)\'s\s+(\w+)\s+ability': r'\1的\2特性',
            
            # 动作相关
            r'switch\s+in': '换入',
            r'switch\s+out': '换出',
            r'set\s+up': '强化',
            r'clean\s+up': '清场',
            r'wall\s+break': '破盾',
            
            # 数值相关
            r'(\d+)\s+HP': r'\1 HP',
            r'(\d+)\s+Attack': r'\1 攻击',
            r'(\d+)\s+Defense': r'\1 防御',
            r'(\d+)\s+Speed': r'\1 速度'
        }
    
    def preprocess_text(self, text: str) -> str:
        """预处理文本，处理复合术语"""
        result = text
        
        # 先处理复合术语（按长度排序，避免部分匹配）
        sorted_compounds = sorted(self.compound_terms.items(), key=lambda x: len(x[0]), reverse=True)
        
        for compound, translation in sorted_compounds:
            # 使用词边界确保精确匹配
            pattern = r'\b' + re.escape(compound) + r'\b'
            result = re.sub(pattern, translation, result, flags=re.IGNORECASE)
        
        return result
    
    def apply_grammar_rules(self, text: str) -> str:
        """应用语法规则"""
        result = text
        
        for pattern, replacement in self.grammar_rules.items():
            def replace_with_translation(match):
                groups = match.groups()
                translated_groups = []
                
                for group in groups:
                    if group and group.strip():
                        # 跳过冠词和介词
                        if group.lower() in ['the', 'a', 'an', 'with', 'as', 'to', 'of', 'in', 'on']:
                            continue
                        # 翻译组中的词汇
                        translated = self.translate_single_word(group)
                        translated_groups.append(translated)
                    else:
                        translated_groups.append('')
                
                # 构建替换字符串
                replacement_str = replacement
                group_index = 1
                for translated_group in translated_groups:
                    if translated_group:
                        replacement_str = replacement_str.replace(f'\\{group_index}', translated_group)
                        group_index += 1
                    else:
                        group_index += 1
                
                return replacement_str
            
            result = re.sub(pattern, replace_with_translation, result, flags=re.IGNORECASE)
        
        return result
    
    def translate_single_word(self, word: str) -> str:
        """翻译单个词汇"""
        word_lower = word.lower().strip()
        return self.dictionary.get(word_lower, word)
    
    def translate_remaining_words(self, text: str) -> str:
        """翻译剩余的单词"""
        # 分词并翻译
        words = re.findall(r'\b\w+\b', text)
        result = text
        
        for word in words:
            translated = self.translate_single_word(word)
            if translated != word:
                # 使用词边界确保精确替换
                pattern = r'\b' + re.escape(word) + r'\b'
                result = re.sub(pattern, translated, result, flags=re.IGNORECASE)
        
        return result
    
    def post_process(self, text: str) -> str:
        """后处理，修正语法和格式"""
        result = text
        
        # 修正常见的语法问题
        corrections = {
            r'携带(\w+)的(\w+)\s+(\w+)': r'携带\3的\2',  # 修正道具描述
            r'(\w+)是一个优秀的(\w+)\s+with\s+(\w+)': r'携带\3的\1是一个优秀的\2',
            r'\s+\.': '。',  # 修正句号
            r'\s+,': '，',  # 修正逗号
            r'\s+;': '；',  # 修正分号
            r'\s+:': '：',  # 修正冒号
            r'\s{2,}': ' ',  # 去除多余空格
        }
        
        for pattern, replacement in corrections.items():
            result = re.sub(pattern, replacement, result)
        
        return result.strip()
    
    def translate_text(self, text: str) -> str:
        """完整翻译文本"""
        if not text.strip():
            return text
        
        # 步骤1: 预处理复合术语
        result = self.preprocess_text(text)
        
        # 步骤2: 应用语法规则
        result = self.apply_grammar_rules(result)
        
        # 步骤3: 翻译剩余单词
        result = self.translate_remaining_words(result)
        
        # 步骤4: 后处理
        result = self.post_process(result)
        
        return result
    
    def translate_paragraph(self, paragraph: str) -> str:
        """翻译段落"""
        # 按句子分割
        sentences = re.split(r'[.!?]+', paragraph)
        translated_sentences = []
        
        for sentence in sentences:
            if sentence.strip():
                translated = self.translate_text(sentence.strip())
                translated_sentences.append(translated)
        
        return '。'.join(translated_sentences) + ('。' if translated_sentences else '')
    
    def translate_document(self, document: str) -> str:
        """翻译整个文档"""
        # 按段落分割
        paragraphs = document.split('\n\n')
        translated_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                translated = self.translate_paragraph(paragraph.strip())
                translated_paragraphs.append(translated)
        
        return '\n\n'.join(translated_paragraphs)
    
    def analyze_translation_quality(self, original: str, translated: str) -> Dict:
        """分析翻译质量"""
        original_words = re.findall(r'\b\w+\b', original.lower())
        total_words = len(original_words)
        
        # 计算已翻译的词汇数
        translated_count = 0
        untranslated_words = []
        
        for word in original_words:
            if word in self.dictionary or word in [k.split()[0] for k in self.compound_terms.keys()]:
                translated_count += 1
            else:
                if word not in untranslated_words:
                    untranslated_words.append(word)
        
        coverage = (translated_count / total_words * 100) if total_words > 0 else 0
        
        # 评估翻译流畅度（简单指标）
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', translated))
        english_chars = len(re.findall(r'[a-zA-Z]', translated))
        fluency_score = (chinese_chars / (chinese_chars + english_chars) * 100) if (chinese_chars + english_chars) > 0 else 0
        
        return {
            'total_words': total_words,
            'translated_words': translated_count,
            'coverage_percentage': round(coverage, 2),
            'fluency_score': round(fluency_score, 2),
            'untranslated_words': untranslated_words[:10],
            'translation_length': len(translated),
            'chinese_ratio': round(chinese_chars / len(translated) * 100, 2) if len(translated) > 0 else 0
        }

def main():
    """主函数 - 演示改进的翻译功能"""
    translator = ImprovedTranslator()
    
    # 测试文本
    test_texts = [
        "Garchomp is a great sweeper with Swords Dance.",
        "This Heatran set is designed to provide special attack coverage with Choice Specs.",
        "Weavile can OHKO Garchomp with Ice Punch after Stealth Rock damage.",
        "Clefable with Magic Guard ability can be used as a special wall.",
        "This team focuses on offensive pressure. Garchomp serves as the primary physical sweeper with Swords Dance setup."
    ]
    
    print("=== 改进版翻译器演示 ===")
    print(f"基础词典: {len(translator.dictionary)} 个术语")
    print(f"复合术语: {len(translator.compound_terms)} 个")
    print(f"语法规则: {len(translator.grammar_rules)} 个")
    print()
    
    results = []
    
    for i, text in enumerate(test_texts, 1):
        print(f"--- 测试 {i} ---")
        print(f"原文: {text}")
        
        # 翻译
        translated = translator.translate_text(text)
        print(f"译文: {translated}")
        
        # 分析质量
        analysis = translator.analyze_translation_quality(text, translated)
        print(f"覆盖率: {analysis['coverage_percentage']}%")
        print(f"流畅度: {analysis['fluency_score']}%")
        print(f"中文比例: {analysis['chinese_ratio']}%")
        
        if analysis['untranslated_words']:
            print(f"未翻译: {', '.join(analysis['untranslated_words'])}")
        
        results.append({
            'original': text,
            'translated': translated,
            'analysis': analysis
        })
        
        print("=" * 50)
        print()
    
    # 保存结果
    report = {
        'test_date': '2025-06-17',
        'translator_type': 'improved_translator_v2.0',
        'capabilities': {
            'basic_dictionary_size': len(translator.dictionary),
            'compound_terms': len(translator.compound_terms),
            'grammar_rules': len(translator.grammar_rules)
        },
        'test_results': results,
        'improvements': [
            '支持复合术语的完整识别',
            '改进的语法规则处理',
            '更好的句子结构转换',
            '后处理修正机制',
            '翻译质量评估'
        ]
    }
    
    with open('improved_translation_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("改进版翻译报告已保存到 improved_translation_report.json")

if __name__ == "__main__":
    main()