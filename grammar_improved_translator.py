#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语法改进版翻译器 - 解决中文语法规范问题
重点改进：
1. 正确的中文语序
2. 合适的助词和连接词
3. 自然的中文表达
4. 完整的语法结构
"""

import json
import re
from typing import Dict, List, Tuple, Optional

class GrammarImprovedTranslator:
    def __init__(self):
        self.dictionary = {}
        self.compound_terms = {}
        self.grammar_rules = {}
        self.sentence_templates = {}
        self.load_translation_data()
        self.build_grammar_system()
    
    def load_translation_data(self):
        """加载翻译数据"""
        try:
            with open('enhanced_translation_results.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.dictionary = data.get('enhanced_dictionary', {})
            print(f"已加载 {len(self.dictionary)} 个术语")
        except:
            print("无法加载翻译数据")
    
    def build_grammar_system(self):
        """构建语法系统"""
        
        # 复合术语（完整短语翻译）
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
            'special attack': '特攻',
            'special defense': '特防',
            'physical attack': '物攻',
            'physical defense': '物防',
            'hidden ability': '隐藏特性',
            'priority move': '先制招式',
            'status move': '变化招式',
            'revenge kill': '报仇击杀',
            'switch in': '换入',
            'switch out': '换出',
            'set up': '强化',
            'clean up': '清场',
            'wall break': '破盾',
            'stealth rock damage': '隐形岩伤害'
        }
        
        # 语法规则和模式
        self.grammar_rules = {
            # 主语 + 是 + 定语 + 名词 + 状语
            'subject_is_adjective_noun_with': {
                'pattern': r'^(\w+)\s+is\s+a\s+(\w+)\s+(\w+)\s+with\s+(.+?)\.$',
                'template': '{subject}是一个{modifier}{noun}，使用{tool}。',
                'process': self.process_subject_is_adjective_noun_with
            },
            
            # 主语 + 可以 + 动作 + 宾语 + 方式 + 条件
            'subject_can_action_object_with_after': {
                'pattern': r'^(\w+)\s+can\s+(\w+)\s+(\w+)\s+with\s+(.+?)\s+after\s+(.+?)\.$',
                'template': '{subject}可以在{condition}后使用{tool}{action}{object}。',
                'process': self.process_subject_can_action_object_with_after
            },
            
            # 主语 + 具有特性 + 可以用作 + 角色
            'subject_with_ability_can_be_used_as': {
                'pattern': r'^(\w+)\s+with\s+(.+?)\s+ability\s+can\s+be\s+used\s+as\s+a\s+(\w+)\s+(\w+)\.$',
                'template': '{subject}具有{ability}特性，可以用作{type}{role}。',
                'process': self.process_subject_with_ability_can_be_used_as
            },
            
            # 这个配置旨在提供...
            'this_set_is_designed_to': {
                'pattern': r'^This\s+(\w+)\s+set\s+is\s+designed\s+to\s+provide\s+(.+?)\s+with\s+(.+?)\.$',
                'template': '这个{pokemon}配置旨在通过{tool}提供{purpose}。',
                'process': self.process_this_set_is_designed_to
            },
            
            # 主语 + 担任 + 角色 + 方式
            'subject_serves_as_role_with': {
                'pattern': r'^(\w+)\s+serves\s+as\s+(?:the\s+)?(\w+)\s+(\w+)\s+(\w+)\s+with\s+(.+?)\s+(\w+)\.$',
                'template': '{subject}担任{modifier}{type}{role}，通过{tool}{method}。',
                'process': self.process_subject_serves_as_role_with
            },
            
            # 主语 + 提供 + 内容
            'subject_provides_content': {
                'pattern': r'^(\w+)\s+provides\s+(\w+)\s+(\w+)\s+(?:coverage\s+)?and\s+(.+?)\s+(\w+)\.$',
                'template': '{subject}提供{type}{content}和{additional}{support}。',
                'process': self.process_subject_provides_content
            },
            
            # 这个队伍专注于...
            'this_team_focuses_on': {
                'pattern': r'^This\s+(\w+)\s+focuses\s+on\s+(\w+)\s+(\w+)\.$',
                'template': '这个{thing}专注于{type}{aspect}。',
                'process': self.process_this_team_focuses_on
            }
        }
    
    def translate_word(self, word: str) -> str:
        """翻译单个词汇"""
        word_lower = word.lower().strip()
        
        # 基础词汇映射
        basic_words = {
            'great': '优秀的',
            'good': '好的',
            'excellent': '卓越的',
            'powerful': '强大的',
            'effective': '有效的',
            'sweeper': '清场手',
            'wall': '盾牌',
            'tank': '坦克',
            'support': '支援',
            'coverage': '打击面',
            'pressure': '压力',
            'offensive': '攻击性',
            'defensive': '防御性',
            'primary': '主要的',
            'main': '主要的',
            'special': '特殊',
            'physical': '物理',
            'ohko': '一击击倒',
            '2hko': '二击击倒',
            'damage': '伤害',
            'setup': '强化',
            'team': '队伍',
            'set': '配置',
            'ability': '特性',
            'move': '招式',
            'attack': '攻击',
            'defense': '防御'
        }
        
        if word_lower in self.dictionary:
            return self.dictionary[word_lower]
        elif word_lower in basic_words:
            return basic_words[word_lower]
        else:
            return word
    
    def preprocess_compounds(self, text: str) -> str:
        """预处理复合术语"""
        result = text
        
        # 按长度排序，先处理长短语
        sorted_compounds = sorted(self.compound_terms.items(), key=lambda x: len(x[0]), reverse=True)
        
        for compound, translation in sorted_compounds:
            pattern = r'\b' + re.escape(compound) + r'\b'
            result = re.sub(pattern, f'[{translation}]', result, flags=re.IGNORECASE)
        
        return result
    
    def process_subject_is_adjective_noun_with(self, groups: tuple) -> Dict[str, str]:
        """处理：主语是形容词名词，使用工具"""
        subject, adjective, noun, tool = groups
        
        return {
            'subject': self.translate_word(subject),
            'modifier': self.translate_word(adjective),
            'noun': self.translate_word(noun),
            'tool': self.translate_phrase(tool)
        }
    
    def process_subject_can_action_object_with_after(self, groups: tuple) -> Dict[str, str]:
        """处理：主语可以动作宾语，使用工具，在条件后"""
        subject, action, obj, tool, condition = groups
        
        return {
            'subject': self.translate_word(subject),
            'action': self.translate_word(action),
            'object': self.translate_word(obj),
            'tool': self.translate_phrase(tool),
            'condition': self.translate_phrase(condition)
        }
    
    def process_subject_with_ability_can_be_used_as(self, groups: tuple) -> Dict[str, str]:
        """处理：主语具有特性，可以用作角色"""
        subject, ability, type_word, role = groups
        
        return {
            'subject': self.translate_word(subject),
            'ability': self.translate_phrase(ability),
            'type': self.translate_word(type_word),
            'role': self.translate_word(role)
        }
    
    def process_this_set_is_designed_to(self, groups: tuple) -> Dict[str, str]:
        """处理：这个配置旨在提供..."""
        pokemon, purpose, tool = groups
        
        return {
            'pokemon': self.translate_word(pokemon),
            'purpose': self.translate_phrase(purpose),
            'tool': self.translate_phrase(tool)
        }
    
    def process_subject_serves_as_role_with(self, groups: tuple) -> Dict[str, str]:
        """处理：主语担任角色，使用方式"""
        subject, modifier, type_word, role, tool, method = groups
        
        return {
            'subject': self.translate_word(subject),
            'modifier': self.translate_word(modifier),
            'type': self.translate_word(type_word),
            'role': self.translate_word(role),
            'tool': self.translate_phrase(tool),
            'method': self.translate_word(method)
        }
    
    def process_subject_provides_content(self, groups: tuple) -> Dict[str, str]:
        """处理：主语提供内容"""
        subject, type_word, content, additional, support = groups
        
        return {
            'subject': self.translate_word(subject),
            'type': self.translate_word(type_word),
            'content': self.translate_word(content),
            'additional': self.translate_phrase(additional),
            'support': self.translate_word(support)
        }
    
    def process_this_team_focuses_on(self, groups: tuple) -> Dict[str, str]:
        """处理：这个队伍专注于..."""
        thing, type_word, aspect = groups
        
        return {
            'thing': self.translate_word(thing),
            'type': self.translate_word(type_word),
            'aspect': self.translate_word(aspect)
        }
    
    def translate_phrase(self, phrase: str) -> str:
        """翻译短语"""
        # 先处理复合术语
        processed = self.preprocess_compounds(phrase)
        
        # 提取已翻译的部分
        translated_parts = re.findall(r'\[([^\]]+)\]', processed)
        remaining = re.sub(r'\[[^\]]+\]', '', processed)
        
        # 翻译剩余单词
        words = re.findall(r'\b\w+\b', remaining)
        translated_words = [self.translate_word(w) for w in words if w]
        
        # 组合结果
        result_parts = translated_parts + [w for w in translated_words if w]
        return ''.join(result_parts)
    
    def apply_grammar_rules(self, text: str) -> str:
        """应用语法规则"""
        text = text.strip()
        
        for rule_name, rule_info in self.grammar_rules.items():
            pattern = rule_info['pattern']
            template = rule_info['template']
            process_func = rule_info['process']
            
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                try:
                    # 处理匹配的组
                    translations = process_func(match.groups())
                    
                    # 应用模板
                    result = template.format(**translations)
                    
                    # 清理格式
                    result = self.clean_translation(result)
                    return result
                    
                except Exception as e:
                    print(f"语法规则 {rule_name} 处理失败: {e}")
                    continue
        
        # 如果没有匹配的语法规则，使用基本翻译
        return self.basic_translate(text)
    
    def basic_translate(self, text: str) -> str:
        """基本翻译方法（改进版）"""
        # 预处理复合术语
        result = self.preprocess_compounds(text)
        
        # 提取已翻译的复合术语
        compound_translations = {}
        compound_matches = re.finditer(r'\[([^\]]+)\]', result)
        for i, match in enumerate(compound_matches):
            placeholder = f'__COMPOUND_{i}__'
            compound_translations[placeholder] = match.group(1)
            result = result.replace(match.group(0), placeholder)
        
        # 翻译剩余单词
        words = re.findall(r'\b\w+\b', result)
        for word in words:
            if not word.startswith('__COMPOUND_'):
                translated = self.translate_word(word)
                if translated != word:
                    pattern = r'\b' + re.escape(word) + r'\b'
                    result = re.sub(pattern, translated, result, flags=re.IGNORECASE)
        
        # 恢复复合术语
        for placeholder, translation in compound_translations.items():
            result = result.replace(placeholder, translation)
        
        # 基本语法调整
        result = self.clean_translation(result)
        return result
    
    def clean_translation(self, text: str) -> str:
        """清理翻译结果"""
        # 移除多余的空格
        text = re.sub(r'\s+', '', text)
        
        # 标点符号转换
        text = re.sub(r'\.$', '。', text)
        text = re.sub(r',$', '，', text)
        text = re.sub(r';$', '；', text)
        text = re.sub(r':$', '：', text)
        
        # 清理重复的助词
        text = re.sub(r'的的+', '的', text)
        text = re.sub(r'，，+', '，', text)
        
        return text
    
    def translate_text(self, text: str) -> str:
        """翻译文本"""
        if not text.strip():
            return text
        
        # 按句子分割
        sentences = re.split(r'[.!?]+', text)
        translated_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # 应用语法规则
                translated = self.apply_grammar_rules(sentence + '.')
                translated_sentences.append(translated)
        
        return ''.join(translated_sentences)
    
    def analyze_translation_quality(self, original: str, translated: str) -> Dict:
        """分析翻译质量"""
        original_words = re.findall(r'\b\w+\b', original.lower())
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', translated)
        english_words = re.findall(r'\b[a-zA-Z]+\b', translated)
        
        total_chars = len(translated)
        chinese_ratio = len(chinese_chars) / total_chars * 100 if total_chars > 0 else 0
        
        # 计算覆盖率
        covered_words = 0
        for word in original_words:
            if word.lower() in self.dictionary or word.lower() in ['the', 'a', 'an', 'is', 'are', 'with', 'and', 'or']:
                covered_words += 1
        
        coverage = covered_words / len(original_words) * 100 if original_words else 0
        
        return {
            'total_words': len(original_words),
            'coverage_percentage': round(coverage, 2),
            'chinese_ratio': round(chinese_ratio, 2),
            'completeness': 100.0 if len(english_words) == 0 else round((1 - len(english_words) / len(original_words)) * 100, 2),
            'translation_length': len(translated),
            'remaining_english_words': len(english_words),
            'grammar_score': self.calculate_grammar_score(translated)
        }
    
    def calculate_grammar_score(self, text: str) -> float:
        """计算语法分数"""
        score = 100.0
        
        # 检查常见语法问题
        issues = [
            (r'[a-zA-Z]+使用[a-zA-Z]+', -10),  # 英文词汇直接连接
            (r'是一个.*使用', -5),  # "是一个...使用" 结构不自然
            (r'可以.*使用.*在.*后', -5),  # 语序问题
            (r'[a-zA-Z]{3,}', -2),  # 未翻译的英文单词
        ]
        
        for pattern, penalty in issues:
            matches = len(re.findall(pattern, text))
            score += matches * penalty
        
        return max(0, min(100, score))

def main():
    """主函数 - 测试语法改进版翻译器"""
    translator = GrammarImprovedTranslator()
    
    # 测试用例
    test_cases = [
        "Garchomp is a great sweeper with Swords Dance.",
        "This Heatran set is designed to provide special attack coverage with Choice Specs.",
        "Weavile can OHKO Garchomp with Ice Punch after Stealth Rock damage.",
        "Clefable with Magic Guard ability can be used as a special wall.",
        "This team focuses on offensive pressure.",
        "Garchomp serves as the primary physical sweeper with Swords Dance setup.",
        "Heatran provides special attack coverage and Stealth Rock support."
    ]
    
    results = []
    
    print("=== 语法改进版翻译器测试 ===")
    print(f"测试时间: {json.dumps('2025-06-17', ensure_ascii=False)}")
    print(f"翻译器版本: grammar_improved_v1.0")
    print()
    
    for i, original in enumerate(test_cases, 1):
        print(f"测试 {i}:")
        print(f"原文: {original}")
        
        translated = translator.translate_text(original)
        analysis = translator.analyze_translation_quality(original, translated)
        
        print(f"译文: {translated}")
        print(f"分析: 覆盖率 {analysis['coverage_percentage']}%, 中文比例 {analysis['chinese_ratio']}%, 语法分数 {analysis['grammar_score']}")
        print()
        
        results.append({
            'original': original,
            'translated': translated,
            'analysis': analysis
        })
    
    # 计算总体统计
    avg_coverage = sum(r['analysis']['coverage_percentage'] for r in results) / len(results)
    avg_chinese_ratio = sum(r['analysis']['chinese_ratio'] for r in results) / len(results)
    avg_grammar_score = sum(r['analysis']['grammar_score'] for r in results) / len(results)
    
    # 保存报告
    report = {
        'test_date': '2025-06-17',
        'translator_version': 'grammar_improved_v1.0',
        'capabilities': {
            'professional_terms': len(translator.dictionary),
            'compound_terms': len(translator.compound_terms),
            'grammar_rules': len(translator.grammar_rules)
        },
        'test_results': results,
        'overall_performance': {
            'average_coverage': round(avg_coverage, 2),
            'average_chinese_ratio': round(avg_chinese_ratio, 2),
            'average_grammar_score': round(avg_grammar_score, 2),
            'total_test_cases': len(results)
        }
    }
    
    with open('grammar_improved_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"总体表现:")
    print(f"平均覆盖率: {avg_coverage:.2f}%")
    print(f"平均中文比例: {avg_chinese_ratio:.2f}%")
    print(f"平均语法分数: {avg_grammar_score:.2f}%")
    print(f"\n详细报告已保存到 grammar_improved_report.json")

if __name__ == '__main__':
    main()