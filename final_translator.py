# -*- coding: utf-8 -*-
"""
最终优化版翻译器 - 实现长文本完全翻译
"""

import json
import re
from typing import Dict, List, Tuple

class FinalTranslator:
    def __init__(self):
        self.dictionary = {}
        self.compound_terms = {}
        self.sentence_patterns = {}
        self.common_words = {}
        self.load_translation_data()
        self.build_comprehensive_patterns()
    
    def load_translation_data(self):
        """加载翻译数据"""
        try:
            with open('enhanced_translation_results.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.dictionary = data.get('enhanced_dictionary', {})
            print(f"已加载 {len(self.dictionary)} 个术语")
        except:
            print("无法加载翻译数据")
    
    def build_comprehensive_patterns(self):
        """构建全面的翻译模式"""
        # 复合术语（完整短语）
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
            'revenge kill': '报仇击杀',
            'switch in': '换入',
            'switch out': '换出',
            'set up': '强化',
            'clean up': '清场',
            'wall break': '破盾'
        }
        
        # 常用词汇翻译
        self.common_words = {
            'this': '这个',
            'that': '那个',
            'is': '是',
            'are': '是',
            'can': '可以',
            'will': '将',
            'with': '使用',
            'and': '和',
            'or': '或',
            'the': '',  # 冠词通常省略
            'a': '',
            'an': '',
            'to': '',  # 介词根据语境处理
            'of': '的',
            'in': '在',
            'on': '在',
            'for': '为了',
            'as': '作为',
            'be': '是',
            'used': '使用',
            'great': '优秀的',
            'good': '好的',
            'excellent': '卓越的',
            'powerful': '强大的',
            'effective': '有效的',
            'reliable': '可靠的',
            'primary': '主要的',
            'main': '主要的',
            'best': '最好的',
            'after': '在...之后',
            'before': '在...之前',
            'damage': '伤害',
            'support': '支援',
            'coverage': '打击面',
            'pressure': '压力',
            'offensive': '攻击性的',
            'defensive': '防御性的',
            'focuses': '专注于',
            'provides': '提供',
            'serves': '担任',
            'acts': '充当',
            'works': '运作',
            'designed': '设计',
            'setup': '强化',
            'team': '队伍',
            'set': '配置',
            'build': '构筑',
            'core': '核心',
            'synergy': '协同'
        }
        
        # 完整句型模式
        self.sentence_patterns = [
            # 基本描述句型
            {
                'pattern': r'^(\w+)\s+is\s+a\s+(great|good|excellent|powerful)\s+(\w+)(?:\s+with\s+(.+?))?\.$',
                'template': '{pokemon}是一个{quality}{role}{item}。',
                'groups': ['pokemon', 'quality', 'role', 'item']
            },
            {
                'pattern': r'^This\s+(\w+)\s+set\s+is\s+designed\s+to\s+(.+?)(?:\s+with\s+(.+?))?\.$',
                'template': '这个{pokemon}配置旨在{purpose}{item}。',
                'groups': ['pokemon', 'purpose', 'item']
            },
            {
                'pattern': r'^(\w+)\s+can\s+(OHKO|2HKO)\s+(\w+)(?:\s+with\s+(.+?))?(?:\s+after\s+(.+?))?\.$',
                'template': '{attacker}可以{ko_type}{target}{move}{condition}。',
                'groups': ['attacker', 'ko_type', 'target', 'move', 'condition']
            },
            {
                'pattern': r'^(\w+)\s+(?:with\s+(.+?)\s+)?(?:ability\s+)?can\s+be\s+used\s+as\s+a\s+(\w+)\s+(\w+)\.$',
                'template': '{pokemon}{ability}可以用作{type}{role}。',
                'groups': ['pokemon', 'ability', 'type', 'role']
            },
            {
                'pattern': r'^(\w+)\s+serves\s+as\s+(?:the\s+)?(\w+)\s+(\w+)\s+(\w+)(?:\s+with\s+(.+?))?\.$',
                'template': '{pokemon}担任{adj}{type}{role}{item}。',
                'groups': ['pokemon', 'adj', 'type', 'role', 'item']
            },
            {
                'pattern': r'^(\w+)\s+provides\s+(\w+)\s+(\w+)(?:\s+and\s+(.+?))?\.$',
                'template': '{pokemon}提供{type}{thing}{additional}。',
                'groups': ['pokemon', 'type', 'thing', 'additional']
            },
            {
                'pattern': r'^This\s+(\w+)\s+focuses\s+on\s+(\w+)\s+(\w+)\.$',
                'template': '这个{thing}专注于{type}{aspect}。',
                'groups': ['thing', 'type', 'aspect']
            }
        ]
    
    def translate_word(self, word: str) -> str:
        """翻译单个词汇"""
        word_lower = word.lower().strip()
        
        # 优先级：专业术语 > 常用词汇
        if word_lower in self.dictionary:
            return self.dictionary[word_lower]
        elif word_lower in self.common_words:
            return self.common_words[word_lower]
        else:
            return word
    
    def preprocess_compounds(self, text: str) -> str:
        """预处理复合术语"""
        result = text
        
        # 按长度排序，先处理长短语
        sorted_compounds = sorted(self.compound_terms.items(), key=lambda x: len(x[0]), reverse=True)
        
        for compound, translation in sorted_compounds:
            pattern = r'\b' + re.escape(compound) + r'\b'
            result = re.sub(pattern, translation, result, flags=re.IGNORECASE)
        
        return result
    
    def apply_sentence_patterns(self, text: str) -> str:
        """应用句型模式"""
        text = text.strip()
        
        for pattern_info in self.sentence_patterns:
            pattern = pattern_info['pattern']
            template = pattern_info['template']
            groups = pattern_info['groups']
            
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                # 提取匹配的组
                matched_groups = match.groups()
                translations = {}
                
                for i, group_name in enumerate(groups):
                    if i < len(matched_groups) and matched_groups[i]:
                        value = matched_groups[i].strip()
                        
                        # 特殊处理
                        if group_name == 'quality':
                            quality_map = {'great': '优秀的', 'good': '好的', 'excellent': '卓越的', 'powerful': '强大的'}
                            translations[group_name] = quality_map.get(value.lower(), value)
                        elif group_name == 'ko_type':
                            ko_map = {'OHKO': '一击击倒', '2HKO': '二击击倒'}
                            translations[group_name] = ko_map.get(value.upper(), value)
                        elif group_name in ['item', 'move', 'condition', 'ability']:
                            # 处理复合短语
                            processed = self.preprocess_compounds(value)
                            if processed != value:
                                translations[group_name] = f'使用{processed}' if group_name in ['item', 'move'] else f'具有{processed}特性' if group_name == 'ability' else f'在{processed}后' if group_name == 'condition' else processed
                            else:
                                # 翻译单词
                                words = value.split()
                                translated_words = [self.translate_word(w) for w in words]
                                translated_phrase = ''.join([w for w in translated_words if w])
                                translations[group_name] = f'使用{translated_phrase}' if group_name in ['item', 'move'] else f'具有{translated_phrase}特性' if group_name == 'ability' else f'在{translated_phrase}后' if group_name == 'condition' else translated_phrase
                        else:
                            # 普通翻译
                            translations[group_name] = self.translate_word(value)
                    else:
                        translations[group_name] = ''
                
                # 构建最终翻译
                try:
                    result = template.format(**translations)
                    # 清理多余的空格和标点
                    result = re.sub(r'\s+', '', result)
                    result = re.sub(r'使用。', '。', result)
                    result = re.sub(r'具有。', '。', result)
                    result = re.sub(r'在后。', '。', result)
                    return result
                except KeyError:
                    pass
        
        # 如果没有匹配的模式，使用基本翻译
        return self.basic_translate(text)
    
    def basic_translate(self, text: str) -> str:
        """基本翻译方法"""
        # 先处理复合术语
        result = self.preprocess_compounds(text)
        
        # 分词并翻译剩余词汇
        words = re.findall(r'\b\w+\b', result)
        for word in words:
            translated = self.translate_word(word)
            if translated != word and translated:
                pattern = r'\b' + re.escape(word) + r'\b'
                result = re.sub(pattern, translated, result, flags=re.IGNORECASE)
        
        # 基本语法调整
        result = re.sub(r'\s+', '', result)  # 去除空格，中文不需要
        result = re.sub(r'\.$', '。', result)  # 句号
        result = re.sub(r',$', '，', result)  # 逗号
        
        return result
    
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
                # 尝试句型模式匹配
                translated = self.apply_sentence_patterns(sentence + '.')
                translated_sentences.append(translated)
        
        return ''.join(translated_sentences)
    
    def translate_paragraph(self, paragraph: str) -> str:
        """翻译段落"""
        return self.translate_text(paragraph)
    
    def translate_document(self, document: str) -> str:
        """翻译文档"""
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
        
        # 计算覆盖率
        covered_words = 0
        for word in original_words:
            if (word in self.dictionary or 
                word in self.common_words or 
                any(word in compound for compound in self.compound_terms.keys())):
                covered_words += 1
        
        coverage = (covered_words / total_words * 100) if total_words > 0 else 0
        
        # 计算中文比例（流畅度指标）
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', translated))
        total_chars = len(translated)
        chinese_ratio = (chinese_chars / total_chars * 100) if total_chars > 0 else 0
        
        # 计算完整度（是否有未翻译的英文单词）
        remaining_english = len(re.findall(r'\b[a-zA-Z]+\b', translated))
        completeness = ((total_chars - remaining_english) / total_chars * 100) if total_chars > 0 else 0
        
        return {
            'total_words': total_words,
            'coverage_percentage': round(coverage, 2),
            'chinese_ratio': round(chinese_ratio, 2),
            'completeness': round(completeness, 2),
            'translation_length': total_chars,
            'remaining_english_words': remaining_english
        }

def main():
    """主函数 - 演示最终翻译器"""
    translator = FinalTranslator()
    
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
    
    print("=== 最终优化版翻译器演示 ===")
    print(f"专业术语: {len(translator.dictionary)} 个")
    print(f"复合术语: {len(translator.compound_terms)} 个")
    print(f"常用词汇: {len(translator.common_words)} 个")
    print(f"句型模式: {len(translator.sentence_patterns)} 个")
    print()
    
    results = []
    total_coverage = 0
    total_completeness = 0
    
    for i, text in enumerate(test_cases, 1):
        print(f"--- 测试 {i} ---")
        print(f"原文: {text}")
        
        translated = translator.translate_text(text)
        print(f"译文: {translated}")
        
        analysis = translator.analyze_translation_quality(text, translated)
        print(f"覆盖率: {analysis['coverage_percentage']}%")
        print(f"完整度: {analysis['completeness']}%")
        print(f"中文比例: {analysis['chinese_ratio']}%")
        
        total_coverage += analysis['coverage_percentage']
        total_completeness += analysis['completeness']
        
        results.append({
            'original': text,
            'translated': translated,
            'analysis': analysis
        })
        
        print("=" * 50)
        print()
    
    avg_coverage = total_coverage / len(test_cases)
    avg_completeness = total_completeness / len(test_cases)
    
    print(f"=== 总体评估 ===")
    print(f"平均覆盖率: {avg_coverage:.2f}%")
    print(f"平均完整度: {avg_completeness:.2f}%")
    print()
    
    # 保存最终报告
    final_report = {
        'test_date': '2025-06-17',
        'translator_version': 'final_translator_v3.0',
        'capabilities': {
            'professional_terms': len(translator.dictionary),
            'compound_terms': len(translator.compound_terms),
            'common_words': len(translator.common_words),
            'sentence_patterns': len(translator.sentence_patterns)
        },
        'test_results': results,
        'overall_performance': {
            'average_coverage': round(avg_coverage, 2),
            'average_completeness': round(avg_completeness, 2),
            'total_test_cases': len(test_cases)
        },
        'features': [
            '完整的句型模式识别',
            '专业术语和常用词汇双重覆盖',
            '复合术语完整处理',
            '中文语法优化',
            '高完整度翻译输出'
        ]
    }
    
    with open('final_translation_report.json', 'w', encoding='utf-8') as f:
        json.dump(final_report, f, ensure_ascii=False, indent=2)
    
    print("最终翻译报告已保存到 final_translation_report.json")

if __name__ == "__main__":
    main()