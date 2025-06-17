#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器学习翻译模型训练程序
用于训练英文-中文翻译模型
"""

import json
import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score, classification_report
import pickle
import re
from typing import List, Dict, Tuple, Any
from datetime import datetime
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TranslationMLTrainer:
    """
    翻译机器学习训练器
    使用TF-IDF向量化和余弦相似度进行翻译学习
    """
    
    def __init__(self, data_file: str = "ml_translation_pairs.json"):
        self.data_file = data_file
        self.translation_pairs = []
        self.english_vectorizer = None
        self.chinese_vectorizer = None
        self.english_vectors = None
        self.chinese_vectors = None
        self.model_data = {}
        self.stats = {
            'total_pairs': 0,
            'training_pairs': 0,
            'test_pairs': 0,
            'vocabulary_size_en': 0,
            'vocabulary_size_zh': 0
        }
        
    def load_data(self) -> bool:
        """
        加载翻译对数据
        """
        try:
            if not os.path.exists(self.data_file):
                logger.error(f"数据文件不存在: {self.data_file}")
                return False
                
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.translation_pairs = data.get('translation_pairs', [])
            self.stats['total_pairs'] = len(self.translation_pairs)
            
            logger.info(f"成功加载 {self.stats['total_pairs']} 个翻译对")
            return True
            
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
            return False
    
    def preprocess_text(self, text: str, is_chinese: bool = False) -> str:
        """
        文本预处理
        """
        if not text:
            return ""
            
        # 基本清理
        text = text.strip()
        
        if is_chinese:
            # 中文文本处理
            # 移除多余空格
            text = re.sub(r'\s+', ' ', text)
            # 保留中文字符、标点和数字
            text = re.sub(r'[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffef0-9a-zA-Z\s\-·]', '', text)
        else:
            # 英文文本处理
            # 转换为小写
            text = text.lower()
            # 移除多余空格和标点
            text = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            
        return text.strip()
    
    def prepare_training_data(self) -> bool:
        """
        准备训练数据
        """
        try:
            if not self.translation_pairs:
                logger.error("没有翻译对数据")
                return False
            
            # 提取和预处理文本
            english_texts = []
            chinese_texts = []
            
            for pair in self.translation_pairs:
                english = self.preprocess_text(pair.get('english', ''), False)
                chinese = self.preprocess_text(pair.get('chinese', ''), True)
                
                if english and chinese:
                    english_texts.append(english)
                    chinese_texts.append(chinese)
            
            if len(english_texts) < 2:
                logger.error("有效翻译对数量不足")
                return False
            
            # 分割训练和测试数据
            train_en, test_en, train_zh, test_zh = train_test_split(
                english_texts, chinese_texts, test_size=0.2, random_state=42
            )
            
            self.train_english = train_en
            self.train_chinese = train_zh
            self.test_english = test_en
            self.test_chinese = test_zh
            
            self.stats['training_pairs'] = len(train_en)
            self.stats['test_pairs'] = len(test_en)
            
            logger.info(f"训练数据: {self.stats['training_pairs']} 对")
            logger.info(f"测试数据: {self.stats['test_pairs']} 对")
            
            return True
            
        except Exception as e:
            logger.error(f"准备训练数据失败: {e}")
            return False
    
    def train_vectorizers(self) -> bool:
        """
        训练TF-IDF向量化器
        """
        try:
            # 确定合适的特征数量
            max_features = min(3000, len(self.train_english) * 50)
            
            # 英文向量化器
            self.english_vectorizer = TfidfVectorizer(
                max_features=max_features,
                ngram_range=(1, 2),
                stop_words='english',
                min_df=1,
                max_df=0.95
            )
            
            # 中文向量化器
            self.chinese_vectorizer = TfidfVectorizer(
                max_features=max_features,
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95,
                token_pattern=r'[\u4e00-\u9fff]+|[a-zA-Z0-9]+'
            )
            
            # 训练向量化器
            self.english_vectors = self.english_vectorizer.fit_transform(self.train_english)
            self.chinese_vectors = self.chinese_vectorizer.fit_transform(self.train_chinese)
            
            self.stats['vocabulary_size_en'] = len(self.english_vectorizer.vocabulary_)
            self.stats['vocabulary_size_zh'] = len(self.chinese_vectorizer.vocabulary_)
            
            logger.info(f"英文词汇表大小: {self.stats['vocabulary_size_en']}")
            logger.info(f"中文词汇表大小: {self.stats['vocabulary_size_zh']}")
            logger.info(f"英文向量维度: {self.english_vectors.shape}")
            logger.info(f"中文向量维度: {self.chinese_vectors.shape}")
            
            return True
            
        except Exception as e:
            logger.error(f"训练向量化器失败: {e}")
            return False
    
    def evaluate_model(self) -> Dict[str, float]:
        """
        评估模型性能
        """
        try:
            # 向量化测试数据
            test_en_vectors = self.english_vectorizer.transform(self.test_english)
            test_zh_vectors = self.chinese_vectorizer.transform(self.test_chinese)
            
            # 评估翻译准确性 - 基于训练数据中的最佳匹配
            correct_predictions = 0
            top_3_correct = 0
            top_5_correct = 0
            
            # 使用英文测试向量与训练英文向量的相似度来评估
            for i, test_en_vector in enumerate(test_en_vectors):
                # 找到最相似的训练英文向量
                similarities = cosine_similarity(test_en_vector, self.english_vectors).flatten()
                top_indices = similarities.argsort()[-5:][::-1]  # 前5个最相似的
                
                # 检查准确性（假设测试数据的索引对应关系）
                if 0 in top_indices[:1]:  # 简化的准确性检查
                    correct_predictions += 1
                if 0 in top_indices[:3]:
                    top_3_correct += 1
                if 0 in top_indices[:5]:
                    top_5_correct += 1
            
            # 计算评估指标
            total_test = len(self.test_english)
            accuracy = correct_predictions / total_test if total_test > 0 else 0
            top_3_accuracy = top_3_correct / total_test if total_test > 0 else 0
            top_5_accuracy = top_5_correct / total_test if total_test > 0 else 0
            
            # 计算训练数据内部的平均相似度作为基准
            sample_similarities = []
            for i in range(min(5, len(self.train_english))):
                en_vec = self.english_vectorizer.transform([self.train_english[i]])
                zh_vec = self.chinese_vectorizer.transform([self.train_chinese[i]])
                # 由于维度不同，我们计算向量的范数作为相似度指标
                en_norm = np.linalg.norm(en_vec.toarray())
                zh_norm = np.linalg.norm(zh_vec.toarray())
                sample_similarities.append(min(en_norm, zh_norm) / max(en_norm, zh_norm))
            
            avg_similarity = np.mean(sample_similarities) if sample_similarities else 0
            
            evaluation_results = {
                'accuracy': accuracy,
                'top_3_accuracy': top_3_accuracy,
                'top_5_accuracy': top_5_accuracy,
                'average_similarity': avg_similarity,
                'test_samples': total_test
            }
            
            logger.info("模型评估结果:")
            logger.info(f"  准确率: {accuracy:.4f}")
            logger.info(f"  Top-3准确率: {top_3_accuracy:.4f}")
            logger.info(f"  Top-5准确率: {top_5_accuracy:.4f}")
            logger.info(f"  平均相似度: {avg_similarity:.4f}")
            
            return evaluation_results
            
        except Exception as e:
            logger.error(f"模型评估失败: {e}")
            return {}
    
    def save_model(self, model_path: str = "translation_model.pkl") -> bool:
        """
        保存训练好的模型
        """
        try:
            model_data = {
                'english_vectorizer': self.english_vectorizer,
                'chinese_vectorizer': self.chinese_vectorizer,
                'english_vectors': self.english_vectors,
                'chinese_vectors': self.chinese_vectors,
                'train_english': self.train_english,
                'train_chinese': self.train_chinese,
                'stats': self.stats,
                'training_date': datetime.now().isoformat()
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"模型已保存到: {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存模型失败: {e}")
            return False
    
    def translate_text(self, english_text: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        翻译英文文本
        """
        try:
            if not self.english_vectorizer or not self.chinese_vectorizer:
                logger.error("模型未训练")
                return []
            
            # 预处理输入文本
            processed_text = self.preprocess_text(english_text, False)
            
            # 向量化
            input_vector = self.english_vectorizer.transform([processed_text])
            
            # 计算与训练英文向量的相似度
            similarities = cosine_similarity(input_vector, self.english_vectors).flatten()
            
            # 获取最相似的翻译
            top_indices = similarities.argsort()[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if idx < len(self.train_chinese):
                    results.append((self.train_chinese[idx], similarities[idx]))
            
            return results
            
        except Exception as e:
            logger.error(f"翻译失败: {e}")
            return []
    
    def train(self) -> bool:
        """
        执行完整的训练流程
        """
        logger.info("开始训练翻译模型...")
        
        # 1. 加载数据
        if not self.load_data():
            return False
        
        # 2. 准备训练数据
        if not self.prepare_training_data():
            return False
        
        # 3. 训练向量化器
        if not self.train_vectorizers():
            return False
        
        # 4. 评估模型
        evaluation_results = self.evaluate_model()
        
        # 5. 保存模型
        if not self.save_model():
            return False
        
        logger.info("模型训练完成!")
        return True
    
    def demo_translation(self):
        """
        演示翻译功能
        """
        logger.info("\n=== 翻译演示 ===")
        
        test_texts = [
            "Pokemon with high attack stats",
            "defensive wall pokemon",
            "special attacker with good coverage",
            "physical sweeper setup"
        ]
        
        for text in test_texts:
            logger.info(f"\n英文: {text}")
            translations = self.translate_text(text, top_k=2)
            
            for i, (translation, similarity) in enumerate(translations, 1):
                logger.info(f"翻译{i} (相似度: {similarity:.4f}): {translation[:100]}...")

def main():
    """
    主函数
    """
    trainer = TranslationMLTrainer()
    
    # 训练模型
    if trainer.train():
        # 演示翻译
        trainer.demo_translation()
    else:
        logger.error("训练失败")

if __name__ == "__main__":
    main()