#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hugging Face Transformers 学习模块
使用预训练的Transformer模型进行翻译学习和生成
支持多种预训练模型：mT5, mBART, MarianMT等
"""

import json
import os
import re
import torch
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass

try:
    from transformers import (
        AutoTokenizer, AutoModelForSeq2SeqLM,
        MT5ForConditionalGeneration, MT5Tokenizer,
        MBartForConditionalGeneration, MBartTokenizer,
        MarianMTModel, MarianTokenizer,
        Trainer, TrainingArguments,
        DataCollatorForSeq2Seq,
        EarlyStoppingCallback
    )
    from torch.utils.data import Dataset
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("警告：Transformers库未安装，请运行: pip install transformers torch")
    TRANSFORMERS_AVAILABLE = False

@dataclass
class TranslationExample:
    """翻译样本数据结构"""
    source_text: str
    target_text: str
    domain: str = "pokemon"  # pokemon, strategy, general
    difficulty: float = 1.0  # 难度评分 0-1
    quality_score: float = 1.0  # 质量评分 0-1

class PokemonTranslationDataset(Dataset):
    """宝可梦翻译数据集"""
    
    def __init__(self, examples: List[TranslationExample], tokenizer, max_length: int = 512):
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        example = self.examples[idx]
        
        # 编码输入文本
        source_encoding = self.tokenizer(
            example.source_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        # 编码目标文本
        target_encoding = self.tokenizer(
            example.target_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        return {
            "input_ids": source_encoding["input_ids"].flatten(),
            "attention_mask": source_encoding["attention_mask"].flatten(),
            "labels": target_encoding["input_ids"].flatten()
        }

class TransformersLearningModule:
    """基于Transformers的学习模块"""
    
    def __init__(self, model_name: str = "google/mt5-small", device: str = "auto"):
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("Transformers库未安装")
        
        self.model_name = model_name
        self.device = self._setup_device(device)
        
        # 初始化模型和分词器
        self.tokenizer = None
        self.model = None
        self.trainer = None
        
        # 数据存储
        self.training_examples: List[TranslationExample] = []
        self.validation_examples: List[TranslationExample] = []
        
        # 学习统计
        self.learning_stats = {
            "total_examples": 0,
            "training_examples": 0,
            "validation_examples": 0,
            "epochs_trained": 0,
            "best_bleu_score": 0.0,
            "model_size": 0,
            "training_time": 0.0
        }
        
        # 专业术语词典
        self.pokemon_terms = {}
        self.move_terms = {}
        self.ability_terms = {}
        self.item_terms = {}
        
        self._initialize_model()
    
    def _setup_device(self, device: str) -> torch.device:
        """设置计算设备"""
        if device == "auto":
            if torch.cuda.is_available():
                return torch.device("cuda")
            elif torch.backends.mps.is_available():  # Apple Silicon
                return torch.device("mps")
            else:
                return torch.device("cpu")
        else:
            return torch.device(device)
    
    def _initialize_model(self):
        """初始化模型和分词器"""
        print(f"正在加载模型: {self.model_name}")
        
        try:
            if "mt5" in self.model_name.lower():
                self.tokenizer = MT5Tokenizer.from_pretrained(self.model_name)
                self.model = MT5ForConditionalGeneration.from_pretrained(self.model_name)
            elif "mbart" in self.model_name.lower():
                self.tokenizer = MBartTokenizer.from_pretrained(self.model_name)
                self.model = MBartForConditionalGeneration.from_pretrained(self.model_name)
            elif "marian" in self.model_name.lower():
                self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
                self.model = MarianMTModel.from_pretrained(self.model_name)
            else:
                # 通用AutoModel
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            
            self.model.to(self.device)
            print(f"模型已加载到设备: {self.device}")
            
            # 计算模型大小
            self.learning_stats["model_size"] = sum(p.numel() for p in self.model.parameters())
            print(f"模型参数量: {self.learning_stats['model_size']:,}")
            
        except Exception as e:
            print(f"模型加载失败: {e}")
            raise
    
    def load_translation_pairs(self, pairs_directory: str = "individual_pairs"):
        """从JSON文件加载翻译对"""
        if not os.path.exists(pairs_directory):
            print(f"目录 {pairs_directory} 不存在")
            return
        
        print(f"正在从 {pairs_directory} 加载翻译对...")
        
        for filename in os.listdir(pairs_directory):
            if filename.endswith('.json'):
                filepath = os.path.join(pairs_directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    if 'english' in data and 'chinese' in data:
                        # 创建翻译样本
                        example = TranslationExample(
                            source_text=data['english'],
                            target_text=data['chinese'],
                            domain=self._classify_domain(data['english']),
                            difficulty=self._assess_difficulty(data['english']),
                            quality_score=self._assess_quality(data['english'], data['chinese'])
                        )
                        
                        # 随机分配到训练集或验证集 (80:20)
                        if np.random.random() < 0.8:
                            self.training_examples.append(example)
                        else:
                            self.validation_examples.append(example)
                        
                        # 提取专业术语
                        self._extract_terms(data['english'], data['chinese'])
                        
                except Exception as e:
                    print(f"加载文件 {filename} 失败: {e}")
                    continue
        
        self.learning_stats["total_examples"] = len(self.training_examples) + len(self.validation_examples)
        self.learning_stats["training_examples"] = len(self.training_examples)
        self.learning_stats["validation_examples"] = len(self.validation_examples)
        
        print(f"成功加载 {self.learning_stats['total_examples']} 个翻译对")
        print(f"训练集: {self.learning_stats['training_examples']} 个")
        print(f"验证集: {self.learning_stats['validation_examples']} 个")
    
    def _classify_domain(self, text: str) -> str:
        """分类文本领域"""
        pokemon_keywords = ['pokemon', 'move', 'ability', 'type', 'stat', 'hp', 'attack', 'defense']
        strategy_keywords = ['strategy', 'team', 'synergy', 'counter', 'check', 'threat']
        
        text_lower = text.lower()
        
        pokemon_count = sum(1 for keyword in pokemon_keywords if keyword in text_lower)
        strategy_count = sum(1 for keyword in strategy_keywords if keyword in text_lower)
        
        if pokemon_count > strategy_count:
            return "pokemon"
        elif strategy_count > 0:
            return "strategy"
        else:
            return "general"
    
    def _assess_difficulty(self, text: str) -> float:
        """评估文本难度"""
        # 基于文本长度、复杂词汇、句子结构等评估难度
        word_count = len(text.split())
        sentence_count = len(re.findall(r'[.!?]+', text))
        
        # 复杂词汇计数
        complex_words = len(re.findall(r'\b\w{8,}\b', text))
        
        # 计算难度分数 (0-1)
        difficulty = min(1.0, (word_count / 100 + complex_words / 10 + sentence_count / 5) / 3)
        return difficulty
    
    def _assess_quality(self, english: str, chinese: str) -> float:
        """评估翻译质量"""
        # 简单的质量评估：基于长度比例和中文字符比例
        en_words = len(english.split())
        cn_chars = len(re.findall(r'[\u4e00-\u9fff]', chinese))
        
        if en_words == 0:
            return 0.0
        
        # 理想的英中长度比例约为 1:1.5
        length_ratio = cn_chars / en_words
        quality = min(1.0, length_ratio / 1.5) if length_ratio <= 3.0 else 0.5
        
        return quality
    
    def _extract_terms(self, english: str, chinese: str):
        """提取专业术语"""
        # 宝可梦名称
        pokemon_pattern = r'\b[A-Z][a-z]+-[A-Z]\b|\bMega [A-Z][a-z]+\b|\b[A-Z][a-z]{4,}\b'
        pokemon_matches = re.findall(pokemon_pattern, english)
        
        # 招式名称
        move_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        move_matches = re.findall(move_pattern, english)
        
        # 简单的术语映射（实际应用中需要更复杂的对齐算法）
        chinese_terms = re.findall(r'[\u4e00-\u9fff]+', chinese)
        
        for i, pokemon in enumerate(pokemon_matches):
            if i < len(chinese_terms):
                self.pokemon_terms[pokemon] = chinese_terms[i]
        
        for i, move in enumerate(move_matches):
            if i < len(chinese_terms):
                self.move_terms[move] = chinese_terms[i]
    
    def fine_tune_model(self, 
                       output_dir: str = "./fine_tuned_model",
                       num_epochs: int = 3,
                       batch_size: int = 8,
                       learning_rate: float = 5e-5,
                       warmup_steps: int = 500,
                       save_steps: int = 1000,
                       eval_steps: int = 500):
        """微调模型"""
        if not self.training_examples:
            print("没有训练数据，请先加载翻译对")
            return
        
        print("开始微调模型...")
        start_time = datetime.now()
        
        # 创建数据集
        train_dataset = PokemonTranslationDataset(
            self.training_examples, self.tokenizer
        )
        
        eval_dataset = None
        if self.validation_examples:
            eval_dataset = PokemonTranslationDataset(
                self.validation_examples, self.tokenizer
            )
        
        # 设置训练参数
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=warmup_steps,
            weight_decay=0.01,
            logging_dir=f"{output_dir}/logs",
            logging_steps=100,
            save_steps=save_steps,
            eval_steps=eval_steps,
            evaluation_strategy="steps" if eval_dataset else "no",
            save_strategy="steps",
            load_best_model_at_end=True if eval_dataset else False,
            metric_for_best_model="eval_loss" if eval_dataset else None,
            learning_rate=learning_rate,
            fp16=torch.cuda.is_available(),  # 使用混合精度训练
            dataloader_pin_memory=True,
            remove_unused_columns=False,
        )
        
        # 数据整理器
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=self.tokenizer,
            model=self.model,
            padding=True
        )
        
        # 创建训练器
        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)] if eval_dataset else None
        )
        
        # 开始训练
        try:
            train_result = self.trainer.train()
            
            # 保存模型
            self.trainer.save_model()
            self.tokenizer.save_pretrained(output_dir)
            
            # 更新统计信息
            end_time = datetime.now()
            self.learning_stats["training_time"] = (end_time - start_time).total_seconds()
            self.learning_stats["epochs_trained"] = num_epochs
            
            print(f"微调完成！训练时间: {self.learning_stats['training_time']:.2f}秒")
            print(f"模型已保存到: {output_dir}")
            
            return train_result
            
        except Exception as e:
            print(f"训练过程中出现错误: {e}")
            raise
    
    def translate_text(self, text: str, max_length: int = 512, num_beams: int = 4) -> str:
        """使用微调后的模型翻译文本"""
        if not self.model or not self.tokenizer:
            raise ValueError("模型未初始化")
        
        # 预处理：应用术语替换
        processed_text = self._preprocess_text(text)
        
        # 编码输入
        inputs = self.tokenizer(
            processed_text,
            return_tensors="pt",
            max_length=max_length,
            truncation=True,
            padding=True
        ).to(self.device)
        
        # 生成翻译
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=num_beams,
                early_stopping=True,
                do_sample=False
            )
        
        # 解码输出
        translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # 后处理：应用术语映射
        final_translation = self._postprocess_translation(translation)
        
        return final_translation
    
    def _preprocess_text(self, text: str) -> str:
        """预处理输入文本"""
        # 标准化文本
        text = re.sub(r'\s+', ' ', text.strip())
        
        # 可以添加更多预处理步骤
        return text
    
    def _postprocess_translation(self, translation: str) -> str:
        """后处理翻译结果"""
        # 应用术语映射
        for en_term, cn_term in self.pokemon_terms.items():
            translation = re.sub(r'\b' + re.escape(en_term) + r'\b', cn_term, translation, flags=re.IGNORECASE)
        
        for en_term, cn_term in self.move_terms.items():
            translation = re.sub(r'\b' + re.escape(en_term) + r'\b', cn_term, translation, flags=re.IGNORECASE)
        
        return translation.strip()
    
    def evaluate_model(self, test_examples: List[TranslationExample] = None) -> Dict[str, float]:
        """评估模型性能"""
        if test_examples is None:
            test_examples = self.validation_examples
        
        if not test_examples:
            print("没有测试数据")
            return {}
        
        print(f"正在评估模型，测试样本数: {len(test_examples)}")
        
        total_score = 0.0
        scores = []
        
        for example in test_examples:
            try:
                predicted = self.translate_text(example.source_text)
                score = self._calculate_similarity(predicted, example.target_text)
                scores.append(score)
                total_score += score
            except Exception as e:
                print(f"评估样本时出错: {e}")
                scores.append(0.0)
        
        avg_score = total_score / len(test_examples) if test_examples else 0.0
        
        evaluation_results = {
            "average_score": avg_score,
            "max_score": max(scores) if scores else 0.0,
            "min_score": min(scores) if scores else 0.0,
            "std_score": np.std(scores) if scores else 0.0,
            "total_samples": len(test_examples)
        }
        
        print(f"评估结果: 平均分数 {avg_score:.3f}")
        return evaluation_results
    
    def _calculate_similarity(self, predicted: str, reference: str) -> float:
        """计算翻译相似度（简单的字符级相似度）"""
        # 简单的字符级Jaccard相似度
        pred_chars = set(predicted)
        ref_chars = set(reference)
        
        if not pred_chars and not ref_chars:
            return 1.0
        
        intersection = len(pred_chars & ref_chars)
        union = len(pred_chars | ref_chars)
        
        return intersection / union if union > 0 else 0.0
    
    def save_learning_report(self, output_path: str = None):
        """保存学习报告"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"transformers_learning_report_{timestamp}.json"
        
        report = {
            "model_info": {
                "model_name": self.model_name,
                "device": str(self.device),
                "model_parameters": self.learning_stats["model_size"]
            },
            "data_info": {
                "total_examples": self.learning_stats["total_examples"],
                "training_examples": self.learning_stats["training_examples"],
                "validation_examples": self.learning_stats["validation_examples"]
            },
            "training_info": {
                "epochs_trained": self.learning_stats["epochs_trained"],
                "training_time_seconds": self.learning_stats["training_time"],
                "best_bleu_score": self.learning_stats["best_bleu_score"]
            },
            "learned_terms": {
                "pokemon_terms": dict(list(self.pokemon_terms.items())[:20]),  # 只保存前20个
                "move_terms": dict(list(self.move_terms.items())[:20]),
                "ability_terms": dict(list(self.ability_terms.items())[:20]),
                "item_terms": dict(list(self.item_terms.items())[:20])
            },
            "generation_timestamp": datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"学习报告已保存到: {output_path}")
        return output_path
    
    def load_pretrained_model(self, model_path: str):
        """加载预训练的微调模型"""
        try:
            print(f"正在加载微调模型: {model_path}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
            self.model.to(self.device)
            
            print("微调模型加载成功")
            
        except Exception as e:
            print(f"加载微调模型失败: {e}")
            raise

def main():
    """主函数 - 演示使用"""
    if not TRANSFORMERS_AVAILABLE:
        print("请先安装Transformers库: pip install transformers torch")
        return
    
    # 创建学习模块
    learning_module = TransformersLearningModule(
        model_name="google/mt5-small",  # 可以改为其他模型
        device="auto"
    )
    
    # 加载翻译对
    learning_module.load_translation_pairs()
    
    if learning_module.training_examples:
        # 微调模型
        learning_module.fine_tune_model(
            num_epochs=2,
            batch_size=4,  # 根据显存调整
            learning_rate=5e-5
        )
        
        # 评估模型
        evaluation_results = learning_module.evaluate_model()
        
        # 测试翻译
        test_text = "Giratina-O is a powerful Ghost/Dragon-type Pokemon with excellent offensive capabilities."
        translation = learning_module.translate_text(test_text)
        print(f"\n测试翻译:")
        print(f"原文: {test_text}")
        print(f"译文: {translation}")
        
        # 保存学习报告
        learning_module.save_learning_report()
    
    else:
        print("没有找到训练数据，请确保individual_pairs目录存在且包含JSON文件")

if __name__ == "__main__":
    main()