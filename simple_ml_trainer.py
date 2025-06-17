#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版机器学习翻译模型训练程序
"""

import json
import os
import re
from collections import Counter
from typing import List, Dict, Tuple
import pickle
from datetime import datetime

class SimpleTranslationTrainer:
    """
    简化的翻译学习器
    使用词频和关键词匹配进行翻译学习
    """
    
    def __init__(self, data_file: str = "ml_translation_pairs.json"):
        self.data_file = data_file
        self.translation_pairs = []
        self.english_keywords = {}
        self.chinese_keywords = {}
        self.translation_map = {}
        self.stats = {
            'total_pairs': 0,
            'english_keywords': 0,
            'chinese_keywords': 0,
            'pokemon_terms': 0
        }
        
    def load_data(self) -> bool:
        """
        加载翻译对数据
        """
        try:
            if not os.path.exists(self.data_file):
                print(f"错误: 数据文件不存在 {self.data_file}")
                return False
                
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.translation_pairs = data.get('translation_pairs', [])
            self.stats['total_pairs'] = len(self.translation_pairs)
            
            print(f"成功加载 {self.stats['total_pairs']} 个翻译对")
            return True
            
        except Exception as e:
            print(f"加载数据失败: {e}")
            return False
    
    def extract_keywords(self, text: str, is_chinese: bool = False) -> List[str]:
        """
        提取关键词
        """
        if not text:
            return []
            
        if is_chinese:
            # 中文关键词提取
            # 移除标点符号，保留中文字符
            text = re.sub(r'[^\u4e00-\u9fff]', ' ', text)
            # 简单的中文分词（按字符）
            words = [char for char in text if char.strip()]
            # 提取2-4字的词组
            keywords = []
            for i in range(len(words)):
                for length in [2, 3, 4]:
                    if i + length <= len(words):
                        word = ''.join(words[i:i+length])
                        if len(word.strip()) == length:
                            keywords.append(word)
            return keywords
        else:
            # 英文关键词提取
            text = text.lower()
            text = re.sub(r'[^a-zA-Z0-9\s-]', ' ', text)
            words = text.split()
            # 过滤停用词和短词
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must'}
            keywords = [word for word in words if len(word) > 2 and word not in stop_words]
            return keywords
    
    def build_keyword_maps(self):
        """
        构建关键词映射
        """
        print("构建关键词映射...")
        
        english_word_count = Counter()
        chinese_word_count = Counter()
        
        # 统计词频
        for pair in self.translation_pairs:
            english_text = pair.get('english', '')
            chinese_text = pair.get('chinese', '')
            
            en_keywords = self.extract_keywords(english_text, False)
            zh_keywords = self.extract_keywords(chinese_text, True)
            
            english_word_count.update(en_keywords)
            chinese_word_count.update(zh_keywords)
            
            # 建立翻译映射
            for en_word in en_keywords:
                if en_word not in self.translation_map:
                    self.translation_map[en_word] = []
                self.translation_map[en_word].append(chinese_text)
        
        # 保存高频关键词
        self.english_keywords = dict(english_word_count.most_common(500))
        self.chinese_keywords = dict(chinese_word_count.most_common(500))
        
        self.stats['english_keywords'] = len(self.english_keywords)
        self.stats['chinese_keywords'] = len(self.chinese_keywords)
        
        print(f"英文关键词: {self.stats['english_keywords']} 个")
        print(f"中文关键词: {self.stats['chinese_keywords']} 个")
    
    def learn_pokemon_terms(self):
        """
        学习宝可梦专业术语
        """
        pokemon_terms = {
            # 基础术语
            'pokemon': '宝可梦',
            'attack': '攻击',
            'defense': '防御',
            'special': '特殊',
            'speed': '速度',
            'hp': 'HP',
            'stats': '种族值',
            'ability': '特性',
            'move': '招式',
            'type': '属性',
            'tier': '分级',
            'meta': '环境',
            'wall': '盾牌',
            'sweeper': '清场手',
            'check': 'check',
            'counter': 'counter',
            'setup': '强化',
            'bulk': '耐久',
            'offensive': '攻击型',
            'defensive': '防御型',
            'physical': '物理',
            'coverage': '打击面',
            'utility': '功能性',
            'pivot': '中转',
            'hazards': '场地危险',
            'stealth rock': '隐形岩',
            'spikes': '撒菱',
            'toxic spikes': '毒菱',
            'entry hazard': '入场危险',
            'boots': '厚底靴',
            'leftovers': '吃剩的东西',
            'choice': '讲究',
            'scarf': '围巾',
            'band': '头带',
            'specs': '眼镜',
            'tera': '太晶',
            'mega': '超级',
            'switch': '换入',
            'revenge': '复仇',
            'ohko': 'OHKO',
            '2hko': '2HKO',
            'damage': '伤害',
            'recovery': '回复',
            'momentum': '节奏'
        }
        
        self.pokemon_terms = pokemon_terms
        self.stats['pokemon_terms'] = len(pokemon_terms)
        print(f"学习了 {self.stats['pokemon_terms']} 个宝可梦术语")
    
    def translate_text(self, english_text: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        翻译英文文本
        """
        if not english_text:
            return []
        
        # 预处理
        text = english_text.lower().strip()
        
        # 查找最匹配的翻译
        matches = []
        
        # 1. 直接术语匹配
        for en_term, zh_term in self.pokemon_terms.items():
            if en_term in text:
                matches.append((zh_term, 1.0))
        
        # 2. 关键词匹配
        keywords = self.extract_keywords(text, False)
        keyword_scores = {}
        
        for keyword in keywords:
            if keyword in self.translation_map:
                for translation in self.translation_map[keyword]:
                    if translation not in keyword_scores:
                        keyword_scores[translation] = 0
                    keyword_scores[translation] += 1
        
        # 按分数排序
        sorted_translations = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 添加到匹配结果
        for translation, score in sorted_translations[:top_k]:
            confidence = min(score / len(keywords), 1.0) if keywords else 0.1
            matches.append((translation[:200] + '...' if len(translation) > 200 else translation, confidence))
        
        # 如果没有找到匹配，返回最相似的翻译
        if not matches and self.translation_pairs:
            # 简单的字符串相似度匹配
            best_match = self.translation_pairs[0]
            matches.append((best_match.get('chinese', '')[:200] + '...', 0.1))
        
        return matches[:top_k]
    
    def save_model(self, model_path: str = "simple_translation_model.pkl") -> bool:
        """
        保存模型
        """
        try:
            model_data = {
                'english_keywords': self.english_keywords,
                'chinese_keywords': self.chinese_keywords,
                'translation_map': self.translation_map,
                'pokemon_terms': self.pokemon_terms,
                'stats': self.stats,
                'training_date': datetime.now().isoformat()
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"模型已保存到: {model_path}")
            return True
            
        except Exception as e:
            print(f"保存模型失败: {e}")
            return False
    
    def train(self) -> bool:
        """
        执行训练
        """
        print("开始训练简化翻译模型...")
        
        # 1. 加载数据
        if not self.load_data():
            return False
        
        # 2. 构建关键词映射
        self.build_keyword_maps()
        
        # 3. 学习宝可梦术语
        self.learn_pokemon_terms()
        
        # 4. 保存模型
        if not self.save_model():
            return False
        
        print("\n训练完成!")
        print(f"总翻译对: {self.stats['total_pairs']}")
        print(f"英文关键词: {self.stats['english_keywords']}")
        print(f"中文关键词: {self.stats['chinese_keywords']}")
        print(f"宝可梦术语: {self.stats['pokemon_terms']}")
        
        return True
    
    def demo_translation(self):
        """
        演示翻译功能
        """
        print("\n=== 翻译演示 ===")
        
        test_texts = [
            "Pokemon with high attack stats",
            "defensive wall pokemon",
            "special attacker with good coverage",
            "physical sweeper setup",
            "stealth rock hazards",
            "choice scarf revenge killer"
        ]
        
        for text in test_texts:
            print(f"\n英文: {text}")
            translations = self.translate_text(text, top_k=2)
            
            if translations:
                for i, (translation, confidence) in enumerate(translations, 1):
                    print(f"翻译{i} (置信度: {confidence:.2f}): {translation}")
            else:
                print("未找到翻译")

def main():
    """
    主函数
    """
    trainer = SimpleTranslationTrainer()
    
    # 训练模型
    if trainer.train():
        # 演示翻译
        trainer.demo_translation()
    else:
        print("训练失败")

if __name__ == "__main__":
    main()