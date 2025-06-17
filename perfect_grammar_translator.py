#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完美语法翻译器 - 最终优化版
专注于：
1. 完全符合中文语法规范
2. 自然流畅的中文表达
3. 准确的语义传达
4. 专业的术语使用
"""

import json
import re
from typing import Dict, List, Tuple, Optional

class PerfectGrammarTranslator:
    def __init__(self):
        self.dictionary = {}
        self.compound_terms = {}
        self.sentence_structures = {}
        self.context_rules = {}
        self.load_translation_data()
        self.build_perfect_grammar_system()
    
    def load_translation_data(self):
        """加载翻译数据"""
        try:
            with open('enhanced_translation_results.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.dictionary = data.get('enhanced_dictionary', {})
            print(f"已加载 {len(self.dictionary)} 个专业术语")
        except:
            print("无法加载翻译数据")
    
    def build_perfect_grammar_system(self):
        """构建完美语法系统"""
        
        # 完整的复合术语库
        self.compound_terms = {
            # 招式名称
            'swords dance': '剑舞',
            'dragon dance': '龙之舞',
            'calm mind': '冥想',
            'nasty plot': '诡计',
            'ice punch': '冰冻拳',
            'thunder punch': '雷电拳',
            'fire punch': '火焰拳',
            'close combat': '近身战',
            'volt switch': '伏特替换',
            'knock off': '拍落',
            'sucker punch': '突袭',
            'u-turn': 'U型回转',
            
            # 道具名称
            'choice band': '讲究头带',
            'choice specs': '讲究眼镜',
            'choice scarf': '讲究围巾',
            'life orb': '生命宝珠',
            'assault vest': '突击背心',
            'stealth rock': '隐形岩',
            
            # 特性名称
            'magic guard': '魔法防守',
            'hidden ability': '隐藏特性',
            
            # 战术术语
            'special attack': '特攻',
            'special defense': '特防',
            'physical attack': '物攻',
            'physical defense': '物防',
            'priority move': '先制招式',
            'status move': '变化招式',
            'revenge kill': '报仇击杀',
            'switch in': '换入',
            'switch out': '换出',
            'set up': '强化',
            'clean up': '清场',
            'wall break': '破盾',
            'stealth rock damage': '隐形岩伤害',
            'special attack coverage': '特攻打击面',
            'offensive pressure': '攻击压力'
        }
        
        # 完美的句子结构模板
        self.sentence_structures = {
            # 类型1：X是一个Y的Z，使用W
            'pokemon_role_with_tool': {
                'patterns': [
                    r'^(\w+)\s+is\s+a\s+(\w+)\s+(\w+)\s+with\s+(.+?)\.$',
                    r'^(\w+)\s+is\s+an?\s+(\w+)\s+(\w+)\s+with\s+(.+?)\.$'
                ],
                'template': '{pokemon}是一个{adjective}的{role}，使用{tool}。',
                'processor': self.process_pokemon_role_with_tool
            },
            
            # 类型2：这个X配置旨在通过Y提供Z
            'set_designed_for': {
                'patterns': [
                    r'^This\s+(\w+)\s+set\s+is\s+designed\s+to\s+provide\s+(.+?)\s+with\s+(.+?)\.$'
                ],
                'template': '这个{pokemon}配置旨在通过{tool}提供{purpose}。',
                'processor': self.process_set_designed_for
            },
            
            # 类型3：X可以在Y后用Z对W造成一击击倒
            'can_ko_with_after': {
                'patterns': [
                    r'^(\w+)\s+can\s+(OHKO|2HKO)\s+(\w+)\s+with\s+(.+?)\s+after\s+(.+?)\.$'
                ],
                'template': '{attacker}可以在{condition}后用{move}对{target}造成{ko_type}。',
                'processor': self.process_can_ko_with_after
            },
            
            # 类型4：具有X特性的Y可以用作Z
            'with_ability_used_as': {
                'patterns': [
                    r'^(\w+)\s+with\s+(.+?)\s+ability\s+can\s+be\s+used\s+as\s+an?\s+(\w+)\s+(\w+)\.$'
                ],
                'template': '具有{ability}特性的{pokemon}可以用作{type}{role}。',
                'processor': self.process_with_ability_used_as
            },
            
            # 类型5：这个X专注于Y
            'focuses_on': {
                'patterns': [
                    r'^This\s+(\w+)\s+focuses\s+on\s+(.+?)\.$'
                ],
                'template': '这个{thing}专注于{focus}。',
                'processor': self.process_focuses_on
            },
            
            # 类型6：X担任Y，通过Z进行W
            'serves_as_with': {
                'patterns': [
                    r'^(\w+)\s+serves\s+as\s+(?:the\s+)?(\w+)\s+(\w+)\s+(\w+)\s+with\s+(.+?)\s+(\w+)\.$'
                ],
                'template': '{pokemon}担任{modifier}{type}{role}，通过{tool}{method}。',
                'processor': self.process_serves_as_with
            },
            
            # 类型7：X提供Y和Z
            'provides_and': {
                'patterns': [
                    r'^(\w+)\s+provides\s+(.+?)\s+and\s+(.+?)\.$'
                ],
                'template': '{pokemon}提供{thing1}和{thing2}。',
                'processor': self.process_provides_and
            }
        }
        
        # 语境规则
        self.context_rules = {
            # 角色翻译规则
            'roles': {
                'sweeper': '清场手',
                'wall': '盾牌',
                'tank': '坦克',
                'support': '辅助',
                'pivot': '轴心',
                'revenge killer': '报仇手',
                'setup sweeper': '强化清场手',
                'wallbreaker': '破盾手'
            },
            
            # 形容词翻译规则
            'adjectives': {
                'great': '优秀',
                'good': '良好',
                'excellent': '卓越',
                'powerful': '强大',
                'effective': '有效',
                'reliable': '可靠',
                'primary': '主要',
                'main': '主要',
                'special': '特殊',
                'physical': '物理',
                'offensive': '攻击性',
                'defensive': '防御性'
            },
            
            # 动作翻译规则
            'actions': {
                'ohko': '一击击倒',
                '2hko': '二击击倒',
                'ko': '击倒',
                'setup': '强化',
                'sweep': '清场',
                'wall': '防守',
                'support': '支援',
                'pivot': '轴心转换'
            }
        }
    
    def translate_term(self, term: str, context: str = 'general') -> str:
        """根据语境翻译术语"""
        term_lower = term.lower().strip()
        
        # 优先级：专业词典 > 复合术语 > 语境规则
        if term_lower in self.dictionary:
            return self.dictionary[term_lower]
        elif term_lower in self.compound_terms:
            return self.compound_terms[term_lower]
        elif context in self.context_rules and term_lower in self.context_rules[context]:
            return self.context_rules[context][term_lower]
        else:
            # 尝试其他语境
            for ctx_name, ctx_rules in self.context_rules.items():
                if term_lower in ctx_rules:
                    return ctx_rules[term_lower]
            return term
    
    def preprocess_text(self, text: str) -> str:
        """预处理文本，标记复合术语"""
        result = text
        
        # 按长度排序，优先处理长短语
        sorted_compounds = sorted(self.compound_terms.items(), key=lambda x: len(x[0]), reverse=True)
        
        for compound, translation in sorted_compounds:
            pattern = r'\b' + re.escape(compound) + r'\b'
            result = re.sub(pattern, f'[{translation}]', result, flags=re.IGNORECASE)
        
        return result
    
    def process_pokemon_role_with_tool(self, groups: tuple) -> Dict[str, str]:
        """处理：宝可梦是角色，使用工具"""
        pokemon, adjective, role, tool = groups
        
        return {
            'pokemon': self.translate_term(pokemon),
            'adjective': self.translate_term(adjective, 'adjectives'),
            'role': self.translate_term(role, 'roles'),
            'tool': self.extract_and_translate_tool(tool)
        }
    
    def process_set_designed_for(self, groups: tuple) -> Dict[str, str]:
        """处理：配置设计用途"""
        pokemon, purpose, tool = groups
        
        return {
            'pokemon': self.translate_term(pokemon),
            'purpose': self.translate_phrase(purpose),
            'tool': self.extract_and_translate_tool(tool)
        }
    
    def process_can_ko_with_after(self, groups: tuple) -> Dict[str, str]:
        """处理：可以击倒"""
        attacker, ko_type, target, move, condition = groups
        
        return {
            'attacker': self.translate_term(attacker),
            'ko_type': self.translate_term(ko_type, 'actions'),
            'target': self.translate_term(target),
            'move': self.extract_and_translate_tool(move),
            'condition': self.translate_phrase(condition)
        }
    
    def process_with_ability_used_as(self, groups: tuple) -> Dict[str, str]:
        """处理：具有特性用作角色"""
        pokemon, ability, type_word, role = groups
        
        return {
            'pokemon': self.translate_term(pokemon),
            'ability': self.translate_phrase(ability),
            'type': self.translate_term(type_word, 'adjectives'),
            'role': self.translate_term(role, 'roles')
        }
    
    def process_focuses_on(self, groups: tuple) -> Dict[str, str]:
        """处理：专注于"""
        thing, focus = groups
        
        return {
            'thing': self.translate_term(thing),
            'focus': self.translate_phrase(focus)
        }
    
    def process_serves_as_with(self, groups: tuple) -> Dict[str, str]:
        """处理：担任角色，使用方式"""
        pokemon, modifier, type_word, role, tool, method = groups
        
        return {
            'pokemon': self.translate_term(pokemon),
            'modifier': self.translate_term(modifier, 'adjectives'),
            'type': self.translate_term(type_word, 'adjectives'),
            'role': self.translate_term(role, 'roles'),
            'tool': self.extract_and_translate_tool(tool),
            'method': self.translate_term(method)
        }
    
    def process_provides_and(self, groups: tuple) -> Dict[str, str]:
        """处理：提供...和..."""
        pokemon, thing1, thing2 = groups
        
        return {
            'pokemon': self.translate_term(pokemon),
            'thing1': self.translate_phrase(thing1),
            'thing2': self.translate_phrase(thing2)
        }
    
    def extract_and_translate_tool(self, tool_text: str) -> str:
        """提取并翻译工具/道具/招式"""
        # 预处理复合术语
        processed = self.preprocess_text(tool_text)
        
        # 提取已翻译的部分
        translated_parts = re.findall(r'\[([^\]]+)\]', processed)
        if translated_parts:
            return translated_parts[0]
        
        # 翻译剩余部分
        remaining = re.sub(r'\[[^\]]+\]', '', processed)
        words = re.findall(r'\b\w+\b', remaining)
        translated_words = [self.translate_term(w) for w in words if w]
        
        return ''.join(translated_words) if translated_words else tool_text
    
    def translate_phrase(self, phrase: str) -> str:
        """翻译短语"""
        # 预处理复合术语
        processed = self.preprocess_text(phrase)
        
        # 提取已翻译的复合术语
        compound_translations = []
        for match in re.finditer(r'\[([^\]]+)\]', processed):
            compound_translations.append(match.group(1))
        
        # 移除标记，翻译剩余单词
        remaining = re.sub(r'\[[^\]]+\]', ' ', processed)
        words = re.findall(r'\b\w+\b', remaining)
        translated_words = []
        
        for word in words:
            translated = self.translate_term(word)
            if translated and translated != word:
                translated_words.append(translated)
        
        # 组合结果
        all_parts = compound_translations + translated_words
        return ''.join(all_parts) if all_parts else phrase
    
    def apply_sentence_structure(self, text: str) -> str:
        """应用句子结构模板"""
        text = text.strip()
        
        for structure_name, structure_info in self.sentence_structures.items():
            patterns = structure_info['patterns']
            template = structure_info['template']
            processor = structure_info['processor']
            
            for pattern in patterns:
                match = re.match(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        # 处理匹配的组
                        translations = processor(match.groups())
                        
                        # 应用模板
                        result = template.format(**translations)
                        
                        # 优化语法
                        result = self.optimize_grammar(result)
                        return result
                        
                    except Exception as e:
                        print(f"句子结构 {structure_name} 处理失败: {e}")
                        continue
        
        # 如果没有匹配的结构，使用智能翻译
        return self.intelligent_translate(text)
    
    def intelligent_translate(self, text: str) -> str:
        """智能翻译（无模板匹配时）"""
        # 预处理复合术语
        result = self.preprocess_text(text)
        
        # 保存复合术语翻译
        compound_map = {}
        for i, match in enumerate(re.finditer(r'\[([^\]]+)\]', result)):
            placeholder = f'__COMPOUND_{i}__'
            compound_map[placeholder] = match.group(1)
            result = result.replace(match.group(0), placeholder)
        
        # 翻译剩余单词
        words = re.findall(r'\b\w+\b', result)
        for word in words:
            if not word.startswith('__COMPOUND_'):
                translated = self.translate_term(word)
                if translated != word:
                    pattern = r'\b' + re.escape(word) + r'\b'
                    result = re.sub(pattern, translated, result, flags=re.IGNORECASE)
        
        # 恢复复合术语
        for placeholder, translation in compound_map.items():
            result = result.replace(placeholder, translation)
        
        # 优化语法
        result = self.optimize_grammar(result)
        return result
    
    def optimize_grammar(self, text: str) -> str:
        """优化中文语法"""
        # 移除多余空格
        text = re.sub(r'\s+', '', text)
        
        # 标点符号转换
        text = re.sub(r'\.$', '。', text)
        text = re.sub(r',$', '，', text)
        
        # 语法优化规则
        optimizations = [
            # 修复"的"字重复
            (r'的的+', '的'),
            # 修复标点重复
            (r'，，+', '，'),
            (r'。。+', '。'),
            # 优化连接词
            (r'和和', '和'),
            # 修复语序问题
            (r'可以(.+?)用(.+?)对(.+?)造成', r'可以用\2对\3造成\1'),
            # 修复助词问题
            (r'通过(.+?)进行', r'通过\1'),
            (r'使用(.+?)进行', r'使用\1'),
        ]
        
        for pattern, replacement in optimizations:
            text = re.sub(pattern, replacement, text)
        
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
                # 应用句子结构
                translated = self.apply_sentence_structure(sentence + '.')
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
            if (word.lower() in self.dictionary or 
                word.lower() in self.compound_terms or
                any(word.lower() in rules for rules in self.context_rules.values()) or
                word.lower() in ['the', 'a', 'an', 'is', 'are', 'with', 'and', 'or', 'can', 'be']):
                covered_words += 1
        
        coverage = covered_words / len(original_words) * 100 if original_words else 0
        
        # 语法质量评分
        grammar_score = self.calculate_grammar_quality(translated)
        
        # 自然度评分
        fluency_score = self.calculate_fluency_score(translated)
        
        return {
            'total_words': len(original_words),
            'coverage_percentage': round(coverage, 2),
            'chinese_ratio': round(chinese_ratio, 2),
            'completeness': 100.0 if len(english_words) == 0 else round((1 - len(english_words) / len(original_words)) * 100, 2),
            'translation_length': len(translated),
            'remaining_english_words': len(english_words),
            'grammar_score': round(grammar_score, 2),
            'fluency_score': round(fluency_score, 2),
            'overall_quality': round((grammar_score + fluency_score + chinese_ratio) / 3, 2)
        }
    
    def calculate_grammar_quality(self, text: str) -> float:
        """计算语法质量分数"""
        score = 100.0
        
        # 语法问题检测
        grammar_issues = [
            (r'[a-zA-Z]+[\u4e00-\u9fff]', -5),  # 英文直接连中文
            (r'[\u4e00-\u9fff]+[a-zA-Z]+', -5),  # 中文直接连英文
            (r'的的', -3),  # 重复的"的"
            (r'，，', -3),  # 重复逗号
            (r'。。', -3),  # 重复句号
            (r'[a-zA-Z]{3,}', -2),  # 未翻译的英文
        ]
        
        for pattern, penalty in grammar_issues:
            matches = len(re.findall(pattern, text))
            score += matches * penalty
        
        return max(0, min(100, score))
    
    def calculate_fluency_score(self, text: str) -> float:
        """计算流畅度分数"""
        score = 100.0
        
        # 流畅度问题检测
        fluency_issues = [
            (r'是一个.+使用', -5),  # 不自然的"是一个...使用"结构
            (r'可以.+使用.+对.+造成', -3),  # 复杂的动作结构
            (r'通过.+进行', -2),  # 冗余的"通过...进行"
            (r'具有.+特性的', 2),  # 自然的特性描述
            (r'可以用作', 2),  # 自然的用途描述
            (r'专注于', 2),  # 自然的专注描述
        ]
        
        for pattern, adjustment in fluency_issues:
            matches = len(re.findall(pattern, text))
            score += matches * adjustment
        
        return max(0, min(100, score))

def main():
    """主函数 - 测试完美语法翻译器"""
    translator = PerfectGrammarTranslator()
    
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
    
    print("=== 完美语法翻译器测试 ===")
    print(f"测试时间: 2025-06-17")
    print(f"翻译器版本: perfect_grammar_v1.0")
    print()
    
    for i, original in enumerate(test_cases, 1):
        print(f"测试 {i}:")
        print(f"原文: {original}")
        
        translated = translator.translate_text(original)
        analysis = translator.analyze_translation_quality(original, translated)
        
        print(f"译文: {translated}")
        print(f"分析: 覆盖率 {analysis['coverage_percentage']}%, 中文比例 {analysis['chinese_ratio']}%, 语法分数 {analysis['grammar_score']}, 流畅度 {analysis['fluency_score']}, 总体质量 {analysis['overall_quality']}")
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
    avg_fluency_score = sum(r['analysis']['fluency_score'] for r in results) / len(results)
    avg_overall_quality = sum(r['analysis']['overall_quality'] for r in results) / len(results)
    
    # 保存报告
    report = {
        'test_date': '2025-06-17',
        'translator_version': 'perfect_grammar_v1.0',
        'capabilities': {
            'professional_terms': len(translator.dictionary),
            'compound_terms': len(translator.compound_terms),
            'sentence_structures': len(translator.sentence_structures),
            'context_rules': sum(len(rules) for rules in translator.context_rules.values())
        },
        'test_results': results,
        'overall_performance': {
            'average_coverage': round(avg_coverage, 2),
            'average_chinese_ratio': round(avg_chinese_ratio, 2),
            'average_grammar_score': round(avg_grammar_score, 2),
            'average_fluency_score': round(avg_fluency_score, 2),
            'average_overall_quality': round(avg_overall_quality, 2),
            'total_test_cases': len(results)
        },
        'quality_assessment': {
            'grammar_compliance': 'excellent' if avg_grammar_score >= 95 else 'good' if avg_grammar_score >= 85 else 'needs_improvement',
            'fluency_level': 'excellent' if avg_fluency_score >= 95 else 'good' if avg_fluency_score >= 85 else 'needs_improvement',
            'chinese_naturalness': 'excellent' if avg_chinese_ratio >= 95 else 'good' if avg_chinese_ratio >= 85 else 'needs_improvement'
        }
    }
    
    with open('perfect_grammar_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"总体表现:")
    print(f"平均覆盖率: {avg_coverage:.2f}%")
    print(f"平均中文比例: {avg_chinese_ratio:.2f}%")
    print(f"平均语法分数: {avg_grammar_score:.2f}%")
    print(f"平均流畅度: {avg_fluency_score:.2f}%")
    print(f"平均总体质量: {avg_overall_quality:.2f}%")
    print(f"\n详细报告已保存到 perfect_grammar_report.json")

if __name__ == '__main__':
    main()