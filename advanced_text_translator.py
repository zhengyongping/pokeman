# -*- coding: utf-8 -*-
"""
高级文本翻译器 - 支持长文本完全翻译
"""

import json
import re
from typing import Dict, List, Tuple

class AdvancedTextTranslator:
    def __init__(self):
        self.dictionary = {}
        self.phrase_patterns = {}
        self.sentence_templates = {}
        self.load_translation_data()
        self.build_translation_patterns()
    
    def load_translation_data(self):
        """加载翻译数据"""
        try:
            with open('enhanced_translation_results.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.dictionary = data.get('enhanced_dictionary', {})
            print(f"已加载 {len(self.dictionary)} 个术语")
        except:
            print("无法加载翻译数据")
    
    def build_translation_patterns(self):
        """构建翻译模式"""
        # 常见短语模式
        self.phrase_patterns = {
            # 宝可梦相关短语
            r'(\w+)\s+set': r'\1配置',
            r'(\w+)\s+build': r'\1构筑',
            r'(\w+)\s+team': r'\1队伍',
            r'(\w+)\s+core': r'\1核心',
            r'(\w+)\s+synergy': r'\1协同',
            
            # 战斗相关短语
            r'switch\s+in': '换入',
            r'switch\s+out': '换出',
            r'set\s+up': '强化',
            r'clean\s+up': '清场',
            r'wall\s+break': '破盾',
            r'revenge\s+kill': '报仇击杀',
            r'priority\s+move': '先制招式',
            r'status\s+move': '变化招式',
            r'physical\s+attack': '物理攻击',
            r'special\s+attack': '特殊攻击',
            r'mixed\s+attack': '双刀攻击',
            
            # 道具相关短语
            r'choice\s+item': '讲究道具',
            r'recovery\s+item': '回复道具',
            r'boosting\s+item': '强化道具',
            
            # 特性相关短语
            r'hidden\s+ability': '隐藏特性',
            r'regular\s+ability': '普通特性',
            
            # 数值相关短语
            r'(\d+)\s+hp': r'\1 HP',
            r'(\d+)\s+attack': r'\1 攻击',
            r'(\d+)\s+defense': r'\1 防御',
            r'(\d+)\s+special\s+attack': r'\1 特攻',
            r'(\d+)\s+special\s+defense': r'\1 特防',
            r'(\d+)\s+speed': r'\1 速度',
        }
        
        # 句子模板
        self.sentence_templates = {
            # 配置描述模板
            r'This\s+(\w+)\s+set\s+is\s+designed\s+to\s+(.+)': r'这个\1配置旨在\2',
            r'(\w+)\s+is\s+a\s+great\s+(\w+)': r'\1是一个优秀的\2',
            r'(\w+)\s+can\s+be\s+used\s+as\s+a\s+(\w+)': r'\1可以用作\2',
            r'(\w+)\s+works\s+well\s+with\s+(\w+)': r'\1与\2配合良好',
            
            # 战斗描述模板
            r'(\w+)\s+can\s+OHKO\s+(\w+)': r'\1可以一击击倒\2',
            r'(\w+)\s+can\s+2HKO\s+(\w+)': r'\1可以二击击倒\2',
            r'(\w+)\s+resists\s+(\w+)': r'\1抗性\2',
            r'(\w+)\s+is\s+weak\s+to\s+(\w+)': r'\1弱点是\2',
            r'(\w+)\s+is\s+immune\s+to\s+(\w+)': r'\1免疫\2',
            
            # 招式描述模板
            r'(\w+)\s+provides\s+(\w+)': r'\1提供\2',
            r'(\w+)\s+gives\s+(\w+)\s+coverage': r'\1给\2提供打击面',
            r'(\w+)\s+is\s+used\s+for\s+(\w+)': r'\1用于\2',
            
            # 道具描述模板
            r'(\w+)\s+holds\s+(\w+)': r'\1携带\2',
            r'(\w+)\s+with\s+(\w+)': r'携带\2的\1',
            
            # 特性描述模板
            r'(\w+)\s+has\s+(\w+)\s+ability': r'\1具有\2特性',
            r'(\w+)\'s\s+(\w+)\s+ability': r'\1的\2特性',
        }
    
    def translate_word(self, word: str) -> str:
        """翻译单个词汇"""
        word_lower = word.lower()
        return self.dictionary.get(word_lower, word)
    
    def translate_phrase(self, text: str) -> str:
        """翻译短语"""
        result = text
        for pattern, replacement in self.phrase_patterns.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result
    
    def translate_sentence_structure(self, text: str) -> str:
        """翻译句子结构"""
        result = text
        for pattern, replacement in self.sentence_templates.items():
            # 先翻译模板中的关键词
            def replace_with_translation(match):
                groups = match.groups()
                translated_groups = []
                for group in groups:
                    # 尝试翻译组中的词汇
                    translated = self.translate_word(group)
                    translated_groups.append(translated)
                
                # 构建替换字符串
                replacement_str = replacement
                for i, translated_group in enumerate(translated_groups, 1):
                    replacement_str = replacement_str.replace(f'\\{i}', translated_group)
                return replacement_str
            
            result = re.sub(pattern, replace_with_translation, result, flags=re.IGNORECASE)
        return result
    
    def translate_remaining_words(self, text: str) -> str:
        """翻译剩余的单词"""
        # 分词并翻译
        words = re.findall(r'\b\w+\b', text)
        result = text
        
        for word in words:
            translated = self.translate_word(word)
            if translated != word:
                # 使用词边界确保精确替换
                pattern = r'\b' + re.escape(word) + r'\b'
                result = re.sub(pattern, translated, result, flags=re.IGNORECASE)
        
        return result
    
    def translate_text(self, text: str) -> str:
        """完整翻译文本"""
        if not text.strip():
            return text
        
        # 步骤1: 翻译句子结构和模板
        result = self.translate_sentence_structure(text)
        
        # 步骤2: 翻译短语
        result = self.translate_phrase(result)
        
        # 步骤3: 翻译剩余的单词
        result = self.translate_remaining_words(result)
        
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
    
    def analyze_translation_coverage(self, text: str) -> Dict:
        """分析翻译覆盖率"""
        words = re.findall(r'\b\w+\b', text.lower())
        total_words = len(words)
        translated_words = 0
        untranslated_words = []
        
        for word in words:
            if word in self.dictionary:
                translated_words += 1
            else:
                if word not in untranslated_words:
                    untranslated_words.append(word)
        
        coverage = (translated_words / total_words * 100) if total_words > 0 else 0
        
        return {
            'total_words': total_words,
            'translated_words': translated_words,
            'coverage_percentage': round(coverage, 2),
            'untranslated_words': untranslated_words[:20]  # 只显示前20个
        }

def main():
    """主函数 - 演示翻译功能"""
    translator = AdvancedTextTranslator()
    
    # 测试文本
    test_texts = [
        "This Garchomp set is designed to sweep teams with Swords Dance.",
        "Dondozo is a great wall that can tank physical attacks effectively.",
        "Heatran with Choice Specs can OHKO most Pokemon with Fire Blast.",
        "Weavile's Ice Punch provides excellent coverage against Dragon types.",
        "This team core works well with Stealth Rock support from Skarmory.",
        "Clefable can be used as a special wall with Magic Guard ability.",
        "Landorus holds Choice Scarf to outspeed faster threats.",
        "The priority move Sucker Punch helps revenge kill weakened opponents.",
        """This is a comprehensive Pokemon team analysis. 
        
        Garchomp serves as the primary physical sweeper with Swords Dance setup. The set includes Earthquake for STAB damage, Dragon Claw for coverage, and Stone Edge to hit Flying types. Choice Band variant can also work for immediate power.
        
        Heatran acts as a special attacker and Stealth Rock setter. With Choice Specs, it can OHKO many Pokemon with Fire Blast or Earth Power. The Steel typing provides valuable resistances to the team.
        
        Clefable functions as a special wall and cleric. Magic Guard ability protects it from hazard damage, while Soft-Boiled provides reliable recovery. Calm Mind sets can also sweep late game."""
    ]
    
    print("=== 高级文本翻译器演示 ===")
    print(f"已加载词典: {len(translator.dictionary)} 个术语")
    print()
    
    for i, text in enumerate(test_texts, 1):
        print(f"--- 测试 {i} ---")
        print(f"原文: {text}")
        print()
        
        # 翻译
        if '\n' in text:
            translated = translator.translate_document(text)
        else:
            translated = translator.translate_text(text)
        
        print(f"译文: {translated}")
        print()
        
        # 分析覆盖率
        analysis = translator.analyze_translation_coverage(text)
        print(f"翻译分析:")
        print(f"  总词数: {analysis['total_words']}")
        print(f"  已翻译: {analysis['translated_words']}")
        print(f"  覆盖率: {analysis['coverage_percentage']}%")
        if analysis['untranslated_words']:
            print(f"  未翻译词汇: {', '.join(analysis['untranslated_words'])}")
        print("=" * 50)
        print()
    
    # 保存翻译器状态
    translator_info = {
        'creation_date': '2025-06-17',
        'translator_type': 'advanced_text_translator',
        'dictionary_size': len(translator.dictionary),
        'phrase_patterns': len(translator.phrase_patterns),
        'sentence_templates': len(translator.sentence_templates),
        'capabilities': {
            'word_translation': True,
            'phrase_translation': True,
            'sentence_structure_translation': True,
            'paragraph_translation': True,
            'document_translation': True,
            'coverage_analysis': True
        },
        'features': [
            '支持单词、短语、句子的完整翻译',
            '智能句子结构识别和转换',
            '段落和文档级别的翻译',
            '翻译覆盖率分析',
            '可扩展的翻译模式'
        ]
    }
    
    with open('advanced_translator_info.json', 'w', encoding='utf-8') as f:
        json.dump(translator_info, f, ensure_ascii=False, indent=2)
    
    print("翻译器信息已保存到 advanced_translator_info.json")

if __name__ == "__main__":
    main()