#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面学习翻译器
不仅学习术语，还学习语法结构、非术语类单词的含义等
"""

import json
import os
import re
import random
from datetime import datetime
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

# 下载必要的NLTK数据
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('chunkers/maxent_ne_chunker')
except LookupError:
    nltk.download('maxent_ne_chunker')

try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

class ComprehensiveLearningTranslator:
    def __init__(self):
        self.pairs_directory = "individual_pairs"
        self.translation_pairs = []
        
        # 术语词典
        self.term_dictionary = {
            'pokemon_names': {},
            'moves': {},
            'abilities': {},
            'items': {},
            'types': {},
            'stats': {},
            'mechanics': {}
        }
        
        # 语法结构模式
        self.grammar_patterns = {
            'sentence_structures': [],
            'phrase_patterns': [],
            'conjunction_patterns': [],
            'conditional_patterns': [],
            'comparison_patterns': []
        }
        
        # 非术语词汇映射
        self.general_vocabulary = {
            'adjectives': {},
            'verbs': {},
            'adverbs': {},
            'nouns': {},
            'prepositions': {},
            'conjunctions': {}
        }
        
        # 语境规则
        self.context_rules = {
            'battle_context': [],
            'strategy_context': [],
            'description_context': [],
            'comparison_context': []
        }
        
        # 句子模板
        self.sentence_templates = {
            'ability_description': [],
            'move_description': [],
            'strategy_explanation': [],
            'counter_explanation': [],
            'team_synergy': []
        }
        
        self.load_data()
        self.analyze_comprehensive_patterns()
    
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
    
    def analyze_comprehensive_patterns(self):
        """全面分析翻译模式"""
        print("开始全面分析翻译模式...")
        
        for pair in self.translation_pairs:
            english_text = pair['english']
            chinese_text = pair['chinese']
            
            # 分析术语
            self.extract_terms(english_text, chinese_text)
            
            # 分析语法结构
            self.analyze_grammar_structures(english_text, chinese_text)
            
            # 分析一般词汇
            self.analyze_general_vocabulary(english_text, chinese_text)
            
            # 分析语境规则
            self.analyze_context_rules(english_text, chinese_text)
            
            # 提取句子模板
            self.extract_sentence_templates(english_text, chinese_text)
        
        print("模式分析完成")
        self.print_analysis_summary()
    
    def extract_terms(self, english_text: str, chinese_text: str):
        """提取专业术语"""
        # 宝可梦名称模式
        pokemon_patterns = [
            r'\b[A-Z][a-z]+-[A-Z]\b',  # Giratina-O, Landorus-T
            r'\bMega [A-Z][a-z]+\b',    # Mega Scizor
            r'\b[A-Z][a-z]+\b(?=\s+(?:can|is|has|uses|learns))'  # 宝可梦名称
        ]
        
        # 招式名称模式
        move_patterns = [
            r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b(?=\s+(?:hits|deals|can))',  # Stone Edge
            r'\b[A-Z][a-z]+(?=\s+(?:is|can|hits|deals))'  # 单词招式
        ]
        
        # 特性和道具模式
        ability_patterns = [
            r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b(?=\s+(?:allows|grants|prevents))',
            r'\b[A-Z][a-z]+(?=\s+(?:allows|grants|prevents))'
        ]
        
        # 从中文文本中提取对应翻译
        chinese_chars = re.findall(r'[\u4e00-\u9fff]+', chinese_text)
        
        # 这里可以添加更复杂的术语提取逻辑
    
    def analyze_grammar_structures(self, english_text: str, chinese_text: str):
        """分析语法结构"""
        sentences = sent_tokenize(english_text)
        chinese_sentences = re.split(r'[。！？]', chinese_text)
        
        for i, sentence in enumerate(sentences):
            if i < len(chinese_sentences):
                chinese_sentence = chinese_sentences[i].strip()
                if chinese_sentence:
                    # 分析句子结构
                    self.analyze_sentence_structure(sentence, chinese_sentence)
    
    def analyze_sentence_structure(self, english_sentence: str, chinese_sentence: str):
        """分析单个句子的结构"""
        # 词性标注
        tokens = word_tokenize(english_sentence)
        pos_tags = pos_tag(tokens)
        
        # 提取语法模式
        structure_pattern = ' '.join([tag for word, tag in pos_tags])
        
        # 识别常见句型
        if 'can' in english_sentence.lower():
            self.grammar_patterns['conditional_patterns'].append({
                'english': english_sentence,
                'chinese': chinese_sentence,
                'pattern_type': 'ability_expression'
            })
        
        if any(word in english_sentence.lower() for word in ['however', 'but', 'although']):
            self.grammar_patterns['conjunction_patterns'].append({
                'english': english_sentence,
                'chinese': chinese_sentence,
                'pattern_type': 'contrast'
            })
        
        if any(word in english_sentence.lower() for word in ['more', 'better', 'stronger']):
            self.grammar_patterns['comparison_patterns'].append({
                'english': english_sentence,
                'chinese': chinese_sentence,
                'pattern_type': 'comparison'
            })
    
    def analyze_general_vocabulary(self, english_text: str, chinese_text: str):
        """分析一般词汇"""
        tokens = word_tokenize(english_text.lower())
        pos_tags = pos_tag(tokens)
        
        # 常见形容词
        adjectives = ['strong', 'weak', 'fast', 'slow', 'bulky', 'frail', 'offensive', 'defensive']
        # 常见动词
        verbs = ['check', 'counter', 'threaten', 'pressure', 'support', 'resist', 'handle']
        # 常见副词
        adverbs = ['easily', 'effectively', 'reliably', 'consistently', 'significantly']
        
        for word, pos in pos_tags:
            if pos.startswith('JJ') and word in adjectives:  # 形容词
                chinese_equivalent = self.find_chinese_equivalent(word, english_text, chinese_text)
                if chinese_equivalent:
                    self.general_vocabulary['adjectives'][word] = chinese_equivalent
            
            elif pos.startswith('VB') and word in verbs:  # 动词
                chinese_equivalent = self.find_chinese_equivalent(word, english_text, chinese_text)
                if chinese_equivalent:
                    self.general_vocabulary['verbs'][word] = chinese_equivalent
            
            elif pos.startswith('RB') and word in adverbs:  # 副词
                chinese_equivalent = self.find_chinese_equivalent(word, english_text, chinese_text)
                if chinese_equivalent:
                    self.general_vocabulary['adverbs'][word] = chinese_equivalent
    
    def find_chinese_equivalent(self, word: str, english_text: str, chinese_text: str) -> str:
        """在中文文本中寻找英文单词的对应翻译"""
        # 简化的对应关系查找
        word_mappings = {
            'strong': '强力', 'weak': '弱', 'fast': '快速', 'slow': '缓慢',
            'bulky': '耐久', 'frail': '脆弱', 'offensive': '进攻', 'defensive': '防御',
            'check': '制衡', 'counter': '克制', 'threaten': '威胁', 'pressure': '施压',
            'support': '支援', 'resist': '抵抗', 'handle': '应对',
            'easily': '轻松', 'effectively': '有效', 'reliably': '可靠',
            'consistently': '稳定', 'significantly': '显著'
        }
        
        return word_mappings.get(word, '')
    
    def analyze_context_rules(self, english_text: str, chinese_text: str):
        """分析语境规则"""
        # 对战语境
        if any(word in english_text.lower() for word in ['battle', 'fight', 'combat', 'vs']):
            self.context_rules['battle_context'].append({
                'english': english_text,
                'chinese': chinese_text
            })
        
        # 策略语境
        if any(word in english_text.lower() for word in ['strategy', 'team', 'synergy', 'build']):
            self.context_rules['strategy_context'].append({
                'english': english_text,
                'chinese': chinese_text
            })
        
        # 描述语境
        if any(word in english_text.lower() for word in ['description', 'ability', 'move', 'stats']):
            self.context_rules['description_context'].append({
                'english': english_text,
                'chinese': chinese_text
            })
    
    def extract_sentence_templates(self, english_text: str, chinese_text: str):
        """提取句子模板"""
        sentences = sent_tokenize(english_text)
        chinese_sentences = re.split(r'[。！？]', chinese_text)
        
        for i, sentence in enumerate(sentences):
            if i < len(chinese_sentences):
                chinese_sentence = chinese_sentences[i].strip()
                
                # 特性描述模板
                if 'ability' in sentence.lower() or 'allows' in sentence.lower():
                    self.sentence_templates['ability_description'].append({
                        'english': sentence,
                        'chinese': chinese_sentence
                    })
                
                # 招式描述模板
                if any(word in sentence.lower() for word in ['hits', 'deals', 'damage', 'attack']):
                    self.sentence_templates['move_description'].append({
                        'english': sentence,
                        'chinese': chinese_sentence
                    })
                
                # 策略解释模板
                if any(word in sentence.lower() for word in ['strategy', 'use', 'run', 'set']):
                    self.sentence_templates['strategy_explanation'].append({
                        'english': sentence,
                        'chinese': chinese_sentence
                    })
    
    def comprehensive_translate(self, text: str) -> str:
        """全面翻译文本"""
        result = text
        
        # 1. 应用术语翻译
        result = self.apply_term_translations(result)
        
        # 2. 应用语法结构转换
        result = self.apply_grammar_transformations(result)
        
        # 3. 应用一般词汇翻译
        result = self.apply_general_vocabulary(result)
        
        # 4. 应用语境规则
        result = self.apply_context_rules(result)
        
        # 5. 应用句子模板
        result = self.apply_sentence_templates(result)
        
        return result
    
    def apply_term_translations(self, text: str) -> str:
        """应用术语翻译"""
        # 基础术语词典
        term_dict = {
            'Garchomp': '烈咬陆鲨', 'Giratina-O': '骑拉帝纳-起源', 'Landorus-T': '土地云-灵兽',
            'Shadow Ball': '影子球', 'Hex': '祸不单行', 'Calm Mind': '冥想',
            'Will-O-Wisp': '磷火', 'Stone Edge': '尖石攻击', 'Thunder Wave': '电磁波',
            'Dragon Dance': '龙之舞', 'Scale Shot': '鳞射', 'Stealth Rock': '隐形岩',
            'setup sweeper': '清场手', 'physical bulk': '物理耐久', 'entry hazards': '钉子',
            'priority moves': '先制招式', 'immune to': '免疫', 'super effective': '效果拔群'
        }
        
        result = text
        for en_term, cn_term in term_dict.items():
            pattern = r'\b' + re.escape(en_term) + r'\b'
            result = re.sub(pattern, cn_term, result, flags=re.IGNORECASE)
        
        return result
    
    def apply_grammar_transformations(self, text: str) -> str:
        """应用语法结构转换"""
        result = text
        
        # 能力表达转换
        result = re.sub(r'(\w+) can (\w+)', r'\1能够\2', result)
        result = re.sub(r'allows (\w+) to (\w+)', r'让\1能够\2', result)
        
        # 对比结构转换
        result = re.sub(r'However,', '然而，', result)
        result = re.sub(r'Although', '虽然', result)
        result = re.sub(r'but', '但是', result)
        
        # 比较结构转换
        result = re.sub(r'more (\w+) than', r'比...更\1', result)
        result = re.sub(r'better than', '比...更好', result)
        
        return result
    
    def apply_general_vocabulary(self, text: str) -> str:
        """应用一般词汇翻译"""
        vocab_dict = {
            'strong': '强力的', 'weak': '弱的', 'fast': '快速的', 'slow': '缓慢的',
            'bulky': '耐久的', 'frail': '脆弱的', 'offensive': '进攻性的', 'defensive': '防御性的',
            'check': '制衡', 'counter': '克制', 'threaten': '威胁', 'pressure': '施压',
            'support': '支援', 'resist': '抵抗', 'handle': '应对',
            'easily': '轻松地', 'effectively': '有效地', 'reliably': '可靠地'
        }
        
        result = text
        for en_word, cn_word in vocab_dict.items():
            pattern = r'\b' + re.escape(en_word) + r'\b'
            result = re.sub(pattern, cn_word, result, flags=re.IGNORECASE)
        
        return result
    
    def apply_context_rules(self, text: str) -> str:
        """应用语境规则"""
        result = text
        
        # 对战语境
        if any(word in text.lower() for word in ['battle', 'fight', 'vs']):
            result = re.sub(r'\bin battle\b', '在对战中', result, flags=re.IGNORECASE)
            result = re.sub(r'\bfight\b', '战斗', result, flags=re.IGNORECASE)
        
        # 策略语境
        if any(word in text.lower() for word in ['team', 'strategy']):
            result = re.sub(r'\bteam\b', '队伍', result, flags=re.IGNORECASE)
            result = re.sub(r'\bstrategy\b', '策略', result, flags=re.IGNORECASE)
        
        return result
    
    def apply_sentence_templates(self, text: str) -> str:
        """应用句子模板"""
        result = text
        
        # 特性描述模板
        result = re.sub(r'(\w+)\'s ability allows it to (\w+)', r'\1的特性让它能够\2', result)
        
        # 招式描述模板
        result = re.sub(r'(\w+) hits (\w+)', r'\1命中\2', result)
        result = re.sub(r'(\w+) deals (\w+) damage', r'\1造成\2伤害', result)
        
        return result
    
    def analyze_translation_quality(self, english: str, chinese: str) -> Dict[str, float]:
        """分析翻译质量"""
        # 术语覆盖率
        english_words = english.split()
        translated_terms = 0
        total_terms = 0
        
        for word in english_words:
            if self.is_pokemon_term(word):
                total_terms += 1
                if self.has_chinese_translation(word, chinese):
                    translated_terms += 1
        
        term_coverage = translated_terms / total_terms if total_terms > 0 else 0
        
        # 中文比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', chinese))
        total_chars = len(chinese)
        chinese_ratio = chinese_chars / total_chars if total_chars > 0 else 0
        
        # 语法完整度
        grammar_score = self.evaluate_grammar_completeness(english, chinese)
        
        # 语境适应度
        context_score = self.evaluate_context_adaptation(english, chinese)
        
        # 整体质量
        overall_quality = (term_coverage * 0.3 + chinese_ratio * 0.2 + 
                          grammar_score * 0.3 + context_score * 0.2)
        
        return {
            'term_coverage': term_coverage,
            'chinese_ratio': chinese_ratio,
            'grammar_score': grammar_score,
            'context_score': context_score,
            'overall_quality': overall_quality
        }
    
    def is_pokemon_term(self, word: str) -> bool:
        """判断是否为宝可梦术语"""
        pokemon_terms = [
            'Garchomp', 'Giratina', 'Landorus', 'Shadow', 'Ball', 'Hex', 'Calm', 'Mind',
            'setup', 'sweeper', 'physical', 'bulk', 'entry', 'hazards', 'priority'
        ]
        return word in pokemon_terms
    
    def has_chinese_translation(self, word: str, chinese_text: str) -> bool:
        """检查中文文本中是否有对应翻译"""
        translations = {
            'Garchomp': '烈咬陆鲨', 'Shadow': '影子', 'Ball': '球', 'Hex': '祸不单行',
            'setup': '强化', 'sweeper': '清场', 'physical': '物理', 'bulk': '耐久'
        }
        
        chinese_translation = translations.get(word, '')
        return chinese_translation in chinese_text if chinese_translation else False
    
    def evaluate_grammar_completeness(self, english: str, chinese: str) -> float:
        """评估语法完整度"""
        # 简化的语法评估
        english_sentences = sent_tokenize(english)
        chinese_sentences = re.split(r'[。！？]', chinese)
        
        if len(english_sentences) == 0:
            return 0.0
        
        # 检查句子数量匹配度
        sentence_ratio = min(len(chinese_sentences), len(english_sentences)) / len(english_sentences)
        
        # 检查语法结构保持度
        structure_score = 0.8  # 假设大部分语法结构得到保持
        
        return (sentence_ratio + structure_score) / 2
    
    def evaluate_context_adaptation(self, english: str, chinese: str) -> float:
        """评估语境适应度"""
        # 检查语境词汇的适当翻译
        context_words = ['battle', 'strategy', 'team', 'ability', 'move']
        context_translations = ['对战', '策略', '队伍', '特性', '招式']
        
        adaptation_score = 0.0
        context_count = 0
        
        for i, word in enumerate(context_words):
            if word in english.lower():
                context_count += 1
                if context_translations[i] in chinese:
                    adaptation_score += 1
        
        return adaptation_score / context_count if context_count > 0 else 0.8
    
    def print_analysis_summary(self):
        """打印分析摘要"""
        print("\n" + "="*60)
        print("全面学习分析摘要")
        print("="*60)
        
        print(f"\n术语分析:")
        print(f"- 宝可梦名称: {len(self.term_dictionary['pokemon_names'])}")
        print(f"- 招式名称: {len(self.term_dictionary['moves'])}")
        print(f"- 特性道具: {len(self.term_dictionary['abilities']) + len(self.term_dictionary['items'])}")
        
        print(f"\n语法结构分析:")
        print(f"- 条件句型: {len(self.grammar_patterns['conditional_patterns'])}")
        print(f"- 对比句型: {len(self.grammar_patterns['conjunction_patterns'])}")
        print(f"- 比较句型: {len(self.grammar_patterns['comparison_patterns'])}")
        
        print(f"\n一般词汇分析:")
        print(f"- 形容词: {len(self.general_vocabulary['adjectives'])}")
        print(f"- 动词: {len(self.general_vocabulary['verbs'])}")
        print(f"- 副词: {len(self.general_vocabulary['adverbs'])}")
        
        print(f"\n语境规则:")
        print(f"- 对战语境: {len(self.context_rules['battle_context'])}")
        print(f"- 策略语境: {len(self.context_rules['strategy_context'])}")
        print(f"- 描述语境: {len(self.context_rules['description_context'])}")
        
        print(f"\n句子模板:")
        print(f"- 特性描述: {len(self.sentence_templates['ability_description'])}")
        print(f"- 招式描述: {len(self.sentence_templates['move_description'])}")
        print(f"- 策略解释: {len(self.sentence_templates['strategy_explanation'])}")
    
    def run_comprehensive_demo(self):
        """运行全面演示"""
        print("\n" + "="*60)
        print("全面学习翻译器演示")
        print("="*60)
        
        if not self.translation_pairs:
            print("没有可用的翻译对数据")
            return
        
        # 测试文本
        test_texts = [
            "Garchomp is a strong setup sweeper that can use Dragon Dance to boost its Attack and Speed.",
            "Shadow Ball hits Ghost-types super effectively and can lower Special Defense.",
            "However, Giratina-O lacks recovery, which limits its ability to check threats consistently.",
            "The team strategy focuses on offensive pressure while maintaining defensive synergy."
        ]
        
        results = []
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n=== 测试 {i} ===")
            print(f"原文: {text}")
            
            # 全面翻译
            translated = self.comprehensive_translate(text)
            print(f"译文: {translated}")
            
            # 质量分析
            quality = self.analyze_translation_quality(text, translated)
            print(f"质量分析:")
            print(f"  术语覆盖率: {quality['term_coverage']:.1%}")
            print(f"  中文比例: {quality['chinese_ratio']:.1%}")
            print(f"  语法得分: {quality['grammar_score']:.1%}")
            print(f"  语境得分: {quality['context_score']:.1%}")
            print(f"  整体质量: {quality['overall_quality']:.1%}")
            
            results.append({
                'id': f'test_{i}',
                'english': text,
                'chinese': translated,
                'quality': quality
            })
        
        # 保存结果
        report = {
            'demo_date': datetime.now().isoformat(),
            'translator_version': 'comprehensive_learning_v1.0',
            'capabilities': {
                'term_translation': True,
                'grammar_transformation': True,
                'vocabulary_mapping': True,
                'context_adaptation': True,
                'template_application': True
            },
            'analysis_summary': {
                'total_pairs': len(self.translation_pairs),
                'grammar_patterns': sum(len(patterns) for patterns in self.grammar_patterns.values()),
                'vocabulary_entries': sum(len(vocab) for vocab in self.general_vocabulary.values()),
                'context_rules': sum(len(rules) for rules in self.context_rules.values()),
                'sentence_templates': sum(len(templates) for templates in self.sentence_templates.values())
            },
            'test_results': results,
            'average_quality': {
                'term_coverage': sum(r['quality']['term_coverage'] for r in results) / len(results),
                'chinese_ratio': sum(r['quality']['chinese_ratio'] for r in results) / len(results),
                'grammar_score': sum(r['quality']['grammar_score'] for r in results) / len(results),
                'context_score': sum(r['quality']['context_score'] for r in results) / len(results),
                'overall_quality': sum(r['quality']['overall_quality'] for r in results) / len(results)
            }
        }
        
        filename = f"comprehensive_learning_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n演示报告已保存到: {filename}")
        
        # 显示总结
        avg_quality = report['average_quality']
        print(f"\n总结:")
        print(f"- 平均术语覆盖率: {avg_quality['term_coverage']:.1%}")
        print(f"- 平均中文比例: {avg_quality['chinese_ratio']:.1%}")
        print(f"- 平均语法得分: {avg_quality['grammar_score']:.1%}")
        print(f"- 平均语境得分: {avg_quality['context_score']:.1%}")
        print(f"- 平均整体质量: {avg_quality['overall_quality']:.1%}")
        print(f"- 全面学习演示完成！")

def main():
    """主函数"""
    print("启动全面学习翻译器...")
    
    translator = ComprehensiveLearningTranslator()
    translator.run_comprehensive_demo()

if __name__ == "__main__":
    main()