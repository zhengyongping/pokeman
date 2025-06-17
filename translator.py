#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英译中个性化翻译程序
支持学习用户翻译风格并生成个性化翻译结果
"""

import json
import os
import re
from typing import Dict, List, Tuple
from collections import defaultdict
import argparse
import time

# 可选依赖，如果没有安装则使用预设样本
try:
    import requests
    from bs4 import BeautifulSoup
    NETWORK_AVAILABLE = True
except ImportError:
    NETWORK_AVAILABLE = False
    print("注意：网络依赖包未安装，将使用预设的Smogon翻译样本")
    print("如需从网络获取内容，请安装: pip install requests beautifulsoup4 lxml")

class PersonalizedTranslator:
    def __init__(self, data_file="translation_data.json"):
        self.data_file = data_file
        self.translation_pairs = []
        self.style_patterns = {
            'formal_words': set(),
            'informal_words': set(),
            'pokemon_terms': {
                # 基础游戏术语
                'pokemon': '宝可梦',
                'trainer': '训练师',
                'gym': '道馆',
                'badge': '徽章',
                'evolution': '进化',
                'legendary': '传说',
                'shiny': '异色',
                'pokeball': '精灵球',
                'battle': '对战',
                'champion': '冠军',
                
                # 能力值术语
                'hp': 'HP',
                'attack': '攻击',
                'defense': '防御',
                'special attack': '特攻',
                'special defense': '特防',
                'speed': '速度',
                'accuracy': '命中率',
                'evasion': '闪避率',
                
                # 基础对战术语
                'move': '招式',
                'ability': '特性',
                'item': '道具',
                'nature': '性格',
                'iv': '个体值',
                'ev': '努力值',
                'burn': '灼伤',
                'poison': '中毒',
                'paralysis': '麻痹',
                'sleep': '睡眠',
                'freeze': '冰冻',
                
                # Smogon竞技术语 (基于官方中文翻译规范)
                'sweeper': '清场手',
                'cleaner': '清场手',
                'wall': '盾牌',
                'walls': '盾牌',
                'wallbreaker': '破盾手',
                'wallbreakers': '破盾手',
                'pivot': '轮转',
                'core': '核心',
                'check': 'check',  # 保持英文，官方建议
                'checks': 'check',
                'counter': 'counter',  # 保持英文，官方建议
                'counters': 'counter',
                'setup': '强化',
                'set up': '强化',
                'stall': '受',
                'offensive': '攻击性',
                'defensive': '防御型',
                'bulk': '耐久',
                'bulky': '耐久型',
                'coverage': '覆盖面',
                'lead': '首发',
                'revenge kill': '反杀',
                'revenge': '反杀',
                'ohko': 'OHKO',
                'outspeed': '超速',
                'outspeeds': '超速',
                'outpace': '超速',
                'outpaces': '超速',
                'predict': '先读',
                'switch': '换人',
                'switching': '换人',
                'entry hazards': '入场伤害',
                'stealth rock': '隐形岩',
                'physical': '物理',
                'special': '特殊',
                'attacker': '攻击手',
                'attackers': '攻击手',
                'glass cannon': '脆皮攻击手',
                'setup sweeper': '强化型清场手',
                'all-out attacker': '四攻手',
                'hyper offensive': 'HO',
                'anti-lead': '针对性首发',
                'balance': '平衡',
                'balanced': '平衡',
                'choice-lock': '锁招',
                'dual screen': '双墙',
                'early game': '开局',
                'mid game': '中局', 
                'late game': '终局',
                'hazard setter': '出钉手',
                'setter': '出钉手',
                'spinblocker': '反扫钉',
                'phazer': '强制换人',
                'shuffler': '强制换人',
                'redirection': '改变目标',
                'speed tie': '同速',
                'switch-in': '换上',
                'teammate': '队友',
                'teammates': '队友',
                'wincon': '胜负手',
                'win condition': '胜负手',
                'cleric': '队医',
                'fodder': '炮灰',
                'lure': '引诱',
                'matchup': '相性',
                'matchups': '相性',
                'metagame': '环境',
                'momentum': '抢节奏',
                'movepool': '技能池',
                'moveslot': '技能位',
                'recovery': '回复',
                'scout': '试探',
                'support': '辅助',
                'tier': '分级',
                'trap': '抓人',
                'trapping': '抓人',
                'typing': '属性组合',
                'user': '使用者',
                'struggle': '挣扎',
                'struggles': '挣扎',
                'against': '对抗',
                'spikes': '撒菱',
                'toxic spikes': '毒菱',
                'hazard setter': '出钉手',
                'tank': '坦克',
                'tanks': '坦克',
                'mixed': '双刀',
                'mixed attacker': '双刀攻击手',
                'utility': '辅助',
                'utility pokemon': '辅助宝可梦',
                'threat': '威胁',
                'threats': '威胁',
                'resist': '抗性',
                'resists': '抵抗',
                'weakness': '弱点',
                'weaknesses': '弱点',
                'immunity': '免疫',
                'immunities': '免疫',
                'favors': '偏爱',
                'favor': '偏爱',
                'spinner': '高速旋转手',
                'momentum': '节奏',
                'matchup': '相性',
                'metagame': '环境',
                'tier': '分级',
                'typing': '属性组合',
                'movepool': '招式池',
                'moveslot': '技能位',
                'choice lock': '锁招',
                'dual screen': '双墙',
                'cleric': '队医',
                'fodder': '炮灰',
                'lure': '引诱',
                'trap': '抓人',
                'phazer': '强制换人',
                'scout': '试探',
                'support': '辅助',
                'win condition': '胜负手'
            },
            'sentence_patterns': [],
            'grammar_preferences': {
                'passive_voice_freq': 0.0,
                'long_sentence_split': True
            }
        }
        self.load_data()
    
    def load_data(self):
        """加载翻译数据和学习模式"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.translation_pairs = data.get('translation_pairs', [])
                    loaded_patterns = data.get('style_patterns', self.style_patterns)
                    
                    # 将list转换回set
                    if 'formal_words' in loaded_patterns:
                        loaded_patterns['formal_words'] = set(loaded_patterns['formal_words'])
                    if 'informal_words' in loaded_patterns:
                        loaded_patterns['informal_words'] = set(loaded_patterns['informal_words'])
                    
                    self.style_patterns.update(loaded_patterns)
                print(f"已加载 {len(self.translation_pairs)} 个翻译样本")
            except Exception as e:
                print(f"加载数据时出错: {e}")
    
    def save_data(self):
        """保存翻译数据和学习模式"""
        # 将set转换为list以支持JSON序列化
        style_patterns_serializable = self.style_patterns.copy()
        style_patterns_serializable['formal_words'] = list(self.style_patterns['formal_words'])
        style_patterns_serializable['informal_words'] = list(self.style_patterns['informal_words'])
        
        data = {
            'translation_pairs': self.translation_pairs,
            'style_patterns': style_patterns_serializable
        }
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("数据已保存")
        except Exception as e:
            print(f"保存数据时出错: {e}")
    
    def add_translation_sample(self, english_text: str, chinese_text: str):
        """添加用户提供的翻译样本并学习风格"""
        self.translation_pairs.append({
            'english': english_text.strip(),
            'chinese': chinese_text.strip()
        })
        
        # 分析翻译风格
        self._analyze_style(english_text, chinese_text)
        print(f"已添加翻译样本，当前共有 {len(self.translation_pairs)} 个样本")
    
    def learn_from_smogon(self, url: str = "https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/"):
        """从Smogon论坛学习翻译内容"""
        if not NETWORK_AVAILABLE:
            print("网络依赖包未安装，使用预设的Smogon翻译样本...")
            self._load_preset_smogon_samples()
            return
        
        print("正在使用高级爬虫从Smogon论坛获取翻译内容...")
        
        try:
            # 尝试使用专门的Smogon爬虫
            try:
                from smogon_scraper import SmogonScraper
                
                scraper = SmogonScraper()
                initial_count = len(self.translation_pairs)
                
                # 爬取翻译内容
                scraper.scrape_chinese_archive(url)
                
                # 将爬取的内容加载到当前翻译器
                scraper.load_into_translator(self)
                
                new_count = len(self.translation_pairs) - initial_count
                print(f"\n高级爬虫学习完成，新增 {new_count} 个翻译样本")
                
                return
                
            except ImportError:
                print("专用爬虫模块未找到，使用基础爬虫...")
            
            # 基础爬虫逻辑（保留原有功能作为备选）
            self._basic_smogon_scraping(url)
            
        except Exception as e:
            print(f"网络请求错误: {e}")
            print("将使用预设的Smogon翻译样本进行学习...")
            self._load_preset_smogon_samples()
            
    def _basic_smogon_scraping(self, url: str):
        """基础的Smogon爬虫功能"""
        # 设置请求头，模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 获取论坛页面
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 查找帖子链接
        post_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and 'threads' in href and not href.startswith('http'):
                full_url = f"https://www.smogon.com{href}"
                post_links.append(full_url)
        
        print(f"找到 {len(post_links)} 个帖子链接")
        
        # 限制处理的帖子数量，避免过度请求
        max_posts = min(5, len(post_links))
        
        for i, post_url in enumerate(post_links[:max_posts]):
            print(f"正在处理第 {i+1}/{max_posts} 个帖子...")
            self._extract_translations_from_post(post_url, headers)
            time.sleep(2)  # 添加延迟，避免请求过于频繁
        
        print(f"基础爬虫学习完成，共获得 {len(self.translation_pairs)} 个翻译样本")
    
    def _extract_translations_from_post(self, post_url: str, headers: dict):
        """从单个帖子中提取翻译内容"""
        if not NETWORK_AVAILABLE:
            return
            
        try:
            response = requests.get(post_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找帖子内容
            post_content = soup.find('div', class_='bbWrapper')
            if not post_content:
                return
            
            # 提取文本内容
            text_content = post_content.get_text(separator='\n', strip=True)
            
            # 尝试识别英文和中文对照的模式
            lines = text_content.split('\n')
            
            for i in range(len(lines) - 1):
                current_line = lines[i].strip()
                next_line = lines[i + 1].strip()
                
                # 检查是否为英文-中文对照
                if (self._is_english_text(current_line) and 
                    self._is_chinese_text(next_line) and 
                    len(current_line) > 10 and len(next_line) > 5):
                    
                    self.add_translation_sample(current_line, next_line)
                    
        except Exception as e:
            print(f"处理帖子时出错: {e}")
    
    def _is_english_text(self, text: str) -> bool:
        """判断文本是否主要为英文"""
        if not text:
            return False
        
        # 计算英文字符比例
        english_chars = sum(1 for c in text if c.isascii() and c.isalpha())
        total_chars = sum(1 for c in text if c.isalpha())
        
        return total_chars > 0 and english_chars / total_chars > 0.7
    
    def _is_chinese_text(self, text: str) -> bool:
        """判断文本是否主要为中文"""
        if not text:
            return False
        
        # 计算中文字符比例
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        total_chars = len(text.replace(' ', ''))
        
        return total_chars > 0 and chinese_chars / total_chars > 0.3
    
    def _load_preset_smogon_samples(self):
        """加载预设的Smogon翻译样本"""
        preset_samples = [
            {
                "english": "This Pokemon is a powerful physical sweeper with great coverage",
                "chinese": "这只宝可梦是强大的物理清场手，拥有出色的覆盖面"
            },
            {
                "english": "Scizor can check most special attackers but struggles against mixed wallbreakers",
                "chinese": "巨钳螳螂能够check大多数特殊攻击手，但在面对双刀破盾手时会陷入苦战"
            },
            {
                "english": "The current metagame favors defensive walls and utility Pokemon",
                "chinese": "当前的环境偏向于防御型墙和工具宝可梦"
            },
            {
                "english": "This setup sweeper can outspeed many threats after a boost",
                "chinese": "这个强化清场手在获得提升后能够超速许多威胁"
            },
            {
                "english": "Garchomp has excellent offensive presence and good coverage moves",
                "chinese": "烈咬陆鲨拥有出色的攻击存在感和良好的覆盖面招式"
            },
            {
                "english": "This balanced team provides good synergy between offensive and defensive cores",
                "chinese": "这个平衡队伍在攻击核心和防御核心之间提供了良好的配合"
            },
            {
                "english": "The revenge killer can clean up weakened opponents effectively",
                "chinese": "这个报复杀手能够有效清理被削弱的对手"
            },
            {
                "english": "Physical attackers struggle against this defensive wall",
                "chinese": "物理攻击手在面对这个防御墙时会陷入苦战"
            }
        ]
        
        for sample in preset_samples:
            self.add_translation_sample(sample["english"], sample["chinese"])
        
        print(f"已加载 {len(preset_samples)} 个预设Smogon翻译样本")
    
    def _analyze_style(self, english_text: str, chinese_text: str):
        """分析翻译风格和模式"""
        # 分析正式/非正式用词
        formal_indicators = ['therefore', 'furthermore', 'consequently', 'nevertheless']
        informal_indicators = ['gonna', 'wanna', 'yeah', 'ok', 'cool']
        
        english_lower = english_text.lower()
        
        for word in formal_indicators:
            if word in english_lower:
                self.style_patterns['formal_words'].add(word)
        
        for word in informal_indicators:
            if word in english_lower:
                self.style_patterns['informal_words'].add(word)
        
        # 分析句子长度偏好
        english_sentences = re.split(r'[.!?]+', english_text)
        chinese_sentences = re.split(r'[。！？]+', chinese_text)
        
        if len(english_sentences) < len(chinese_sentences):
            self.style_patterns['grammar_preferences']['long_sentence_split'] = True
        
        # 分析被动语态使用频率
        passive_patterns = [r'\bis\s+\w+ed\b', r'\bwas\s+\w+ed\b', r'\bare\s+\w+ed\b', r'\bwere\s+\w+ed\b']
        passive_count = sum(len(re.findall(pattern, english_text, re.IGNORECASE)) for pattern in passive_patterns)
        
        if passive_count > 0:
            current_freq = self.style_patterns['grammar_preferences']['passive_voice_freq']
            self.style_patterns['grammar_preferences']['passive_voice_freq'] = (current_freq + 1) / 2
    
    def basic_translate(self, english_text: str) -> str:
        """基础翻译功能（简化版本）"""
        # 这里是一个简化的翻译实现，实际应用中应该使用专业的翻译API或模型
        basic_dict = {
            
        }
        
        # 合并宝可梦术语到基础词典
        basic_dict.update(self.style_patterns['pokemon_terms'])
        
        # 简单的词汇替换翻译
        words = re.findall(r'\b\w+\b', english_text.lower())
        translated_words = []
        
        for word in words:
            if word in basic_dict:
                translated_words.append(basic_dict[word])
            else:
                translated_words.append(f"[{word}]")
        
        return ''.join(translated_words)
    
    def personalized_translate(self, english_text: str) -> str:
        """基于学习风格的个性化翻译"""
        # 首先进行基础翻译
        base_translation = self.basic_translate(english_text)
        
        # 如果没有学习样本，返回基础翻译
        if not self.translation_pairs:
            return base_translation
        
        # 应用宝可梦术语
        personalized_translation = self._apply_pokemon_terms(base_translation, english_text)
        
        # 应用学习到的风格
        personalized_translation = self._apply_learned_style(personalized_translation, english_text)
        
        # 查找相似的翻译样本
        similar_translation = self._find_similar_translation(english_text)
        if similar_translation:
            return f"{personalized_translation} (参考学习样本: {similar_translation})"
        
        return personalized_translation
    
    def _apply_pokemon_terms(self, translation: str, english_text: str) -> str:
        """应用宝可梦专业术语"""
        result = translation
        english_lower = english_text.lower()
        
        for eng_term, chi_term in self.style_patterns['pokemon_terms'].items():
            if eng_term in english_lower:
                # 替换对应的翻译
                result = result.replace(f"[{eng_term}]", chi_term)
        
        return result
    
    def _apply_learned_style(self, translation: str, english_text: str) -> str:
        """应用学习到的翻译风格"""
        result = translation
        
        # 根据正式/非正式风格调整
        english_lower = english_text.lower()
        
        formal_count = sum(1 for word in self.style_patterns['formal_words'] if word in english_lower)
        informal_count = sum(1 for word in self.style_patterns['informal_words'] if word in english_lower)
        
        if formal_count > informal_count:
            result = result.replace('你', '您')
        
        # 根据句子拆分偏好调整
        if self.style_patterns['grammar_preferences']['long_sentence_split']:
            # 在适当位置添加句号
            result = re.sub(r'([，、])', r'\1 ', result)
        
        return result
    
    def _find_similar_translation(self, english_text: str) -> str:
        """查找相似的翻译样本"""
        english_words = set(re.findall(r'\b\w+\b', english_text.lower()))
        
        best_match = None
        best_score = 0
        
        for pair in self.translation_pairs:
            sample_words = set(re.findall(r'\b\w+\b', pair['english'].lower()))
            
            # 计算词汇重叠度
            overlap = len(english_words & sample_words)
            total = len(english_words | sample_words)
            
            if total > 0:
                score = overlap / total
                if score > best_score and score > 0.3:  # 至少30%相似度
                    best_score = score
                    best_match = pair['chinese']
        
        return best_match
    
    def show_learning_progress(self):
        """显示学习进度"""
        print("\n=== 学习进度 ===")
        print(f"翻译样本数量: {len(self.translation_pairs)}")
        print(f"正式用词: {len(self.style_patterns['formal_words'])}")
        print(f"非正式用词: {len(self.style_patterns['informal_words'])}")
        print(f"被动语态使用频率: {self.style_patterns['grammar_preferences']['passive_voice_freq']:.2f}")
        print(f"长句拆分偏好: {self.style_patterns['grammar_preferences']['long_sentence_split']}")
        
        if self.translation_pairs:
            print("\n最近的翻译样本:")
            for i, pair in enumerate(self.translation_pairs[-3:], 1):
                print(f"{i}. EN: {pair['english'][:3000]}...")
                print(f"   CN: {pair['chinese'][:3000]}...")

def main():
    parser = argparse.ArgumentParser(description='英译中个性化翻译程序')
    parser.add_argument('--learn', action='store_true', help='学习模式：添加翻译样本')
    parser.add_argument('--learn-smogon', action='store_true', help='从Smogon论坛学习翻译内容')
    parser.add_argument('--translate', type=str, help='翻译指定的英文文本')
    parser.add_argument('--progress', action='store_true', help='显示学习进度')
    parser.add_argument('--interactive', action='store_true', help='交互模式')
    
    args = parser.parse_args()
    
    translator = PersonalizedTranslator()
    
    if args.learn_smogon:
        print("=== Smogon论坛学习模式 ===")
        translator.learn_from_smogon()
        translator.save_data()
        
    elif args.learn:
        print("=== 手动学习模式 ===")
        print("选择学习方式:")
        print("1. 手动输入翻译样本")
        print("2. 从Smogon论坛自动学习")
        
        choice = input("请选择 (1/2): ").strip()
        
        if choice == '2':
            translator.learn_from_smogon()
            translator.save_data()
        else:
            print("请输入英文原文和期望的中文译文（输入'quit'退出）")
            
            while True:
                english = input("\n英文原文: ").strip()
                if english.lower() == 'quit':
                    break
                
                chinese = input("期望译文: ").strip()
                if chinese.lower() == 'quit':
                    break
                
                if english and chinese:
                    translator.add_translation_sample(english, chinese)
                    translator.save_data()
                else:
                    print("请输入有效的文本")
    
    elif args.translate:
        print(f"\n原文: {args.translate}")
        print(f"基础翻译: {translator.basic_translate(args.translate)}")
        print(f"个性化翻译: {translator.personalized_translate(args.translate)}")
    
    elif args.progress:
        translator.show_learning_progress()
    
    elif args.interactive:
        print("=== 交互翻译模式 ===")
        print("输入英文文本进行翻译（输入'quit'退出，'learn'进入学习模式，'progress'查看进度）")
        
        while True:
            user_input = input("\n> ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'learn':
                english = input("英文原文: ").strip()
                chinese = input("期望译文: ").strip()
                if english and chinese:
                    translator.add_translation_sample(english, chinese)
                    translator.save_data()
            elif user_input.lower() == 'progress':
                translator.show_learning_progress()
            elif user_input:
                print(f"基础翻译: {translator.basic_translate(user_input)}")
                print(f"个性化翻译: {translator.personalized_translate(user_input)}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()