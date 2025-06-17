# -*- coding: utf-8 -*-
"""
URL翻译器
根据输入的Smogon论坛URL，爬取first post内容并使用学习结果进行中文翻译
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from typing import Dict, List, Any
import os

class URLTranslator:
    def __init__(self):
        # 初始化HTTP会话
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # 加载学习到的翻译知识
        self.load_learned_knowledge()
        
    def load_learned_knowledge(self):
        """加载学习到的翻译知识"""
        # 精确的术语词典
        self.term_dictionary = {
            'pokemon_names': {
                'Garchomp': '烈咬陆鲨',
                'Giratina-O': '骑拉帝纳-起源',
                'Giratina': '骑拉帝纳',
                'Landorus-T': '土地云-灵兽',
                'Landorus': '土地云',
                'Clefable': '皮可西',
                'Heatran': '席多蓝恩',
                'Scizor': '巨钳螳螂',
                'Kartana': '纸御剑',
                'Zapdos': '闪电鸟',
                'Ho-Oh': '凤王',
                'Arceus': '阿尔宙斯',
                'Kyogre': '盖欧卡',
                'Koraidon': '故勒顿',
                'Miraidon': '密勒顿',
                'Necrozma-DM': '奈克洛兹玛-黄昏之鬃',
                'Ting-Lu': '古鼎鹿',
                'Gliscor': '天蝎王',
                'Chien-Pao': '古剑豹',
                'Clodsire': '土王'
            },
            'move_names': {
                'Shadow Ball': '影子球',
                'Dragon Dance': '龙之舞',
                'Calm Mind': '冥想',
                'Will-O-Wisp': '磷火',
                'Stone Edge': '尖石攻击',
                'Thunder Wave': '电磁波',
                'Scale Shot': '鳞射',
                'Stealth Rock': '隐形岩',
                'Hex': '祸不单行',
                'Poltergeist': '灵骚',
                'Dragon Tail': '龙尾',
                'Defog': '清雾',
                'Shadow Sneak': '影子偷袭',
                'Shadow Claw': '影爪',
                'Draco Meteor': '流星群',
                'Extreme Speed': '神速',
                'Knock Off': '拍落',
                'Taunt': '挑衅',
                'Ruination': '大灾难',
                'Flare Blitz': '闪焰冲锋',
                'Toxic': '剧毒'
            },
            'abilities': {
                'Levitate': '飘浮',
                'Griseous Core': '反转核心'
            },
            'items': {
                'Griseous Core': '白金宝珠',
                'Life Orb': '生命宝珠',
                'Choice Band': '讲究头带',
                'Choice Specs': '讲究眼镜',
                'Leftovers': '吃剩的东西'
            },
            'battle_terms': {
                'setup sweeper': '强化清场手',
                'physical bulk': '物理耐久',
                'special bulk': '特殊耐久',
                'entry hazards': '入场危险',
                'priority moves': '先制招式',
                'super effective': '效果拔群',
                'not very effective': '效果不佳',
                'immune to': '免疫',
                'STAB': '本系加成',
                'Ghost-types': '幽灵系',
                'Dragon-types': '龙系',
                'Steel-types': '钢系',
                'Poison-types': '毒系',
                'Fairy-types': '妖精系',
                'Ground-types': '地面系',
                'Fire-types': '火系',
                'Electric-types': '电系',
                'Terastallization': '太晶化',
                'Tera Steel': '太晶钢',
                'Tera Ghost': '太晶幽灵',
                'Tera Poison': '太晶毒',
                'wallbreakers': '破墙手',
                'defensive cores': '防御核心',
                'chip damage': '削弱伤害'
            }
        }
        
        # 一般词汇
        self.general_vocabulary = {
            'adjectives': {
                'strong': '强力的',
                'powerful': '强大的',
                'effective': '有效的',
                'reliable': '可靠的',
                'consistent': '稳定的',
                'versatile': '多样的',
                'bulky': '耐久的',
                'frail': '脆弱的',
                'offensive': '进攻性的',
                'defensive': '防御性的',
                'notable': '值得注意的',
                'distinct': '独特的',
                'unique': '独特的',
                'high': '高的',
                'low': '低的',
                'great': '很好的',
                'excellent': '优秀的',
                'fantastic': '极好的',
                'immense': '巨大的',
                'critical': '关键的',
                'useful': '有用的',
                'valuable': '有价值的',
                'tanky': '坦克型的'
            },
            'verbs': {
                'check': '制衡',
                'counter': '克制',
                'threaten': '威胁',
                'pressure': '施压',
                'support': '支援',
                'handle': '应对',
                'cover': '覆盖',
                'boost': '提升',
                'lower': '降低',
                'hits': '命中',
                'lacks': '缺乏',
                'limits': '限制',
                'provides': '提供',
                'enables': '使能够',
                'maintains': '维持',
                'negates': '否定',
                'allows': '允许',
                'combined': '结合',
                'access': '获得',
                'resist': '抵抗',
                'appreciate': '欣赏',
                'shrug off': '摆脱',
                'take out': '击败',
                'turn the tide': '扭转局势',
                'finish off': '击败',
                'add up': '累积',
                'reduce': '减少'
            },
            'adverbs': {
                'effectively': '有效地',
                'reliably': '可靠地',
                'consistently': '稳定地',
                'significantly': '显著地',
                'easily': '轻松地',
                'extremely': '极其',
                'notably': '值得注意地',
                'particularly': '特别地',
                'potentially': '潜在地',
                'otherwise': '否则'
            },
            'nouns': {
                'recovery': '回复',
                'ability': '能力',
                'threats': '威胁',
                'team': '队伍',
                'strategy': '策略',
                'weakness': '弱点',
                'Attack': '攻击',
                'Defense': '防御',
                'Speed': '速度',
                'HP': '体力',
                'niche': '定位',
                'typing': '属性',
                'standards': '标准',
                'disposal': '支配',
                'utility': '实用性',
                'tier': '分级',
                'combination': '组合',
                'advantage': '优势',
                'management': '管理',
                'options': '选择',
                'mention': '提及',
                'partners': '搭档',
                'damage': '伤害',
                'time': '时间',
                'picture': '情况'
            }
        }
        
        # 语法结构映射
        self.grammar_structures = {
            'ability_expressions': {
                r'(\w+) is (.+?) to (.+)': r'\1能够\3',
                r'(\w+) can (.+)': r'\1能够\2',
                r'access to (.+)': r'获得\1'
            },
            'comparison_expressions': {
                r'However, (.+)': r'然而，\1',
                r'While (.+), (.+)': r'虽然\1，但是\2',
                r'Although (.+), (.+)': r'尽管\1，\2'
            },
            'descriptive_expressions': {
                r'most notable for (.+)': r'最值得注意的是\1',
                r'makes up for (.+) with (.+)': r'用\2弥补\1',
                r'in combination with (.+)': r'与\1结合'
            }
        }
        
    def scrape_first_post(self, url: str) -> Dict[str, str]:
        """爬取指定URL的first post内容"""
        try:
            print(f"正在爬取URL: {url}")
            
            # 发送请求
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 获取帖子标题
            title_elem = soup.find('h1', class_='p-title-value')
            title = title_elem.get_text(strip=True) if title_elem else "未知标题"
            
            # 查找第一个帖子内容
            first_post = soup.find('div', class_='bbWrapper')
            
            if not first_post:
                raise Exception("未找到帖子内容")
            
            # 提取纯文本内容
            text_content = first_post.get_text(separator='\n', strip=True)
            
            # 清理文本格式
            lines = text_content.split('\n')
            cleaned_lines = []
            for line in lines:
                cleaned_line = re.sub(r'\s+', ' ', line.strip())
                if cleaned_line:  # 只保留非空行
                    cleaned_lines.append(cleaned_line)
            
            cleaned_content = '\n'.join(cleaned_lines)
            
            print(f"成功爬取帖子: {title}")
            print(f"内容长度: {len(cleaned_content)} 字符")
            
            return {
                'title': title,
                'content': cleaned_content,
                'url': url
            }
            
        except Exception as e:
            print(f"爬取失败: {e}")
            return None
    
    def translate_text(self, text: str) -> str:
        """翻译英文文本为中文"""
        result = text
        
        # 1. 应用术语翻译（按长度降序排序以避免部分匹配）
        all_terms = {}
        for category in self.term_dictionary.values():
            all_terms.update(category)
        
        sorted_terms = sorted(all_terms.items(), key=lambda x: len(x[0]), reverse=True)
        
        for en_term, cn_term in sorted_terms:
            pattern = r'\b' + re.escape(en_term) + r'\b'
            result = re.sub(pattern, cn_term, result, flags=re.IGNORECASE)
        
        # 2. 应用语法结构转换
        for category, patterns in self.grammar_structures.items():
            for pattern, replacement in patterns.items():
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # 3. 应用一般词汇翻译
        all_vocab = {}
        for category in self.general_vocabulary.values():
            all_vocab.update(category)
        
        sorted_vocab = sorted(all_vocab.items(), key=lambda x: len(x[0]), reverse=True)
        
        for en_word, cn_word in sorted_vocab:
            pattern = r'\b' + re.escape(en_word) + r'\b'
            result = re.sub(pattern, cn_word, result, flags=re.IGNORECASE)
        
        return result
    
    def analyze_translation_quality(self, english: str, chinese: str) -> Dict[str, float]:
        """分析翻译质量"""
        # 计算中文字符比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', chinese))
        total_chars = len(chinese.replace(' ', ''))
        chinese_ratio = chinese_chars / total_chars if total_chars > 0 else 0
        
        # 计算术语覆盖率
        all_terms = set()
        for category in self.term_dictionary.values():
            all_terms.update(category.keys())
        
        found_terms = sum(1 for term in all_terms if term.lower() in english.lower())
        translated_terms = sum(1 for term_dict in self.term_dictionary.values() 
                             for cn_term in term_dict.values() if cn_term in chinese)
        
        term_coverage = translated_terms / found_terms if found_terms > 0 else 0
        
        # 语法得分
        grammar_indicators = ['能够', '然而', '虽然', '尽管', '与', '结合']
        grammar_score = min(1.0, sum(1 for indicator in grammar_indicators if indicator in chinese) * 0.2)
        
        # 总体质量
        overall_quality = (chinese_ratio * 0.3 + term_coverage * 0.4 + grammar_score * 0.3)
        
        return {
            'chinese_ratio': chinese_ratio,
            'term_coverage': term_coverage,
            'grammar_score': grammar_score,
            'overall_quality': overall_quality
        }
    
    def process_url(self, url: str) -> Dict[str, Any]:
        """处理单个URL，爬取并翻译"""
        # 爬取内容
        scraped_data = self.scrape_first_post(url)
        if not scraped_data:
            return None
        
        # 翻译内容
        print("\n正在翻译内容...")
        translated_content = self.translate_text(scraped_data['content'])
        
        # 分析质量
        quality = self.analyze_translation_quality(scraped_data['content'], translated_content)
        
        result = {
            'url': url,
            'title': scraped_data['title'],
            'original_content': scraped_data['content'],
            'translated_content': translated_content,
            'translation_quality': quality,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"翻译完成，质量评分: {quality['overall_quality']:.3f}")
        
        return result
    
    def save_result(self, result: Dict[str, Any], output_file: str = None):
        """保存翻译结果"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'url_translation_{timestamp}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n结果已保存到: {output_file}")
        
    def interactive_mode(self):
        """交互模式"""
        print("=== URL翻译器 - 交互模式 ===")
        print("输入Smogon论坛URL来爬取和翻译first post内容")
        print("输入 'quit' 退出程序\n")
        
        while True:
            url = input("请输入URL: ").strip()
            
            if url.lower() == 'quit':
                print("程序退出")
                break
            
            if not url:
                print("请输入有效的URL")
                continue
            
            if 'smogon.com' not in url:
                print("请输入Smogon论坛的URL")
                continue
            
            print("\n" + "="*50)
            result = self.process_url(url)
            
            if result:
                print(f"\n标题: {result['title']}")
                print(f"\n原文内容 (前200字符):")
                print(result['original_content'][:200] + "..." if len(result['original_content']) > 200 else result['original_content'])
                print(f"\n翻译内容:")
                print(result['translated_content'])
                print(f"\n翻译质量:")
                print(f"  中文比例: {result['translation_quality']['chinese_ratio']:.3f}")
                print(f"  术语覆盖率: {result['translation_quality']['term_coverage']:.3f}")
                print(f"  语法得分: {result['translation_quality']['grammar_score']:.3f}")
                print(f"  总体质量: {result['translation_quality']['overall_quality']:.3f}")
                
                # 询问是否保存
                save_choice = input("\n是否保存结果? (y/n): ").strip().lower()
                if save_choice == 'y':
                    self.save_result(result)
            else:
                print("处理失败")
            
            print("\n" + "="*50 + "\n")

def main():
    """主函数"""
    translator = URLTranslator()
    
    # 检查命令行参数
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"处理URL: {url}")
        result = translator.process_url(url)
        if result:
            translator.save_result(result)
    else:
        # 交互模式
        translator.interactive_mode()

if __name__ == '__main__':
    main()