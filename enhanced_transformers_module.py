#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版Transformers学习模块
集成配置管理、多模型支持、高级评估指标等功能
"""

import json
import os
import re
import torch
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional, Union
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import logging

try:
    from transformers import (
        AutoTokenizer, AutoModelForSeq2SeqLM,
        MT5ForConditionalGeneration, MT5Tokenizer,
        MBartForConditionalGeneration, MBartTokenizer,
        MarianMTModel, MarianTokenizer,
        Trainer, TrainingArguments,
        DataCollatorForSeq2Seq,
        EarlyStoppingCallback,
        get_linear_schedule_with_warmup
    )
    from torch.utils.data import Dataset, DataLoader
    import sacrebleu
    TRANSFORMERS_AVAILABLE = True
except ImportError as e:
    print(f"警告：部分依赖库未安装: {e}")
    print("请运行: pip install transformers torch sacrebleu")
    TRANSFORMERS_AVAILABLE = False

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EnhancedTranslationExample:
    """增强版翻译样本"""
    source_text: str
    target_text: str
    domain: str = "general"
    difficulty: float = 1.0
    quality_score: float = 1.0
    source_file: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class ModelConfig:
    """模型配置"""
    name: str
    description: str
    parameters: str
    memory_requirement: str
    recommended_batch_size: int
    max_length: int
    languages: List[str]
    use_case: str

@dataclass
class TrainingConfig:
    """训练配置"""
    num_epochs: int
    learning_rate: float
    warmup_steps: int
    save_steps: int
    eval_steps: int
    description: str

class EnhancedPokemonDataset(Dataset):
    """增强版宝可梦翻译数据集"""
    
    def __init__(self, 
                 examples: List[EnhancedTranslationExample], 
                 tokenizer, 
                 max_length: int = 512,
                 source_lang: str = "en",
                 target_lang: str = "zh"):
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.source_lang = source_lang
        self.target_lang = target_lang
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        example = self.examples[idx]
        
        # 为mBART模型添加语言标记
        source_text = example.source_text
        target_text = example.target_text
        
        if hasattr(self.tokenizer, 'lang_code_to_id'):
            # mBART模型
            source_text = f"{self.source_lang}_XX {source_text}"
            target_text = f"{self.target_lang}_CN {target_text}"
        
        # 编码输入
        source_encoding = self.tokenizer(
            source_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        # 编码目标
        with self.tokenizer.as_target_tokenizer():
            target_encoding = self.tokenizer(
                target_text,
                max_length=self.max_length,
                padding="max_length",
                truncation=True,
                return_tensors="pt"
            )
        
        labels = target_encoding["input_ids"]
        labels[labels == self.tokenizer.pad_token_id] = -100
        
        return {
            "input_ids": source_encoding["input_ids"].flatten(),
            "attention_mask": source_encoding["attention_mask"].flatten(),
            "labels": labels.flatten(),
            "difficulty": torch.tensor(example.difficulty, dtype=torch.float),
            "quality_score": torch.tensor(example.quality_score, dtype=torch.float)
        }

class EnhancedTransformersModule:
    """增强版Transformers学习模块"""
    
    def __init__(self, 
                 config_path: str = "transformers_config.json",
                 model_key: str = "mt5_small",
                 device: str = "auto"):
        
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("Transformers库未安装")
        
        # 加载配置
        self.config = self._load_config(config_path)
        self.model_config = ModelConfig(**self.config["models"][model_key])
        self.device = self._setup_device(device)
        
        # 初始化模型组件
        self.tokenizer = None
        self.model = None
        self.trainer = None
        
        # 数据存储
        self.training_examples: List[EnhancedTranslationExample] = []
        self.validation_examples: List[EnhancedTranslationExample] = []
        self.test_examples: List[EnhancedTranslationExample] = []
        
        # 专业术语词典
        self.term_dictionaries = {
            'pokemon_names': {},
            'moves': {},
            'abilities': {},
            'items': {},
            'types': {},
            'stats': {},
            'mechanics': {},
            'strategies': {}
        }
        
        # 学习统计
        self.learning_stats = {
            "model_info": asdict(self.model_config),
            "total_examples": 0,
            "training_examples": 0,
            "validation_examples": 0,
            "test_examples": 0,
            "epochs_trained": 0,
            "best_scores": {},
            "training_time": 0.0,
            "evaluation_history": []
        }
        
        self._initialize_model()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"配置文件 {config_path} 不存在，使用默认配置")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"配置文件格式错误: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "models": {
                "mt5_small": {
                    "name": "google/mt5-small",
                    "description": "多语言T5小型模型",
                    "parameters": "300M",
                    "memory_requirement": "2GB",
                    "recommended_batch_size": 8,
                    "max_length": 512,
                    "languages": ["en", "zh"],
                    "use_case": "development"
                }
            },
            "training_configs": {
                "development": {
                    "num_epochs": 3,
                    "learning_rate": 3e-5,
                    "warmup_steps": 500,
                    "save_steps": 1000,
                    "eval_steps": 500,
                    "description": "开发配置"
                }
            }
        }
    
    def _setup_device(self, device: str) -> torch.device:
        """设置计算设备"""
        if device == "auto":
            if torch.cuda.is_available():
                device_name = torch.device("cuda")
                logger.info(f"使用GPU: {torch.cuda.get_device_name()}")
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                device_name = torch.device("mps")
                logger.info("使用Apple Silicon GPU")
            else:
                device_name = torch.device("cpu")
                logger.info("使用CPU")
        else:
            device_name = torch.device(device)
        
        return device_name
    
    def _initialize_model(self):
        """初始化模型"""
        model_name = self.model_config.name
        logger.info(f"正在加载模型: {model_name}")
        
        try:
            if "mt5" in model_name.lower():
                self.tokenizer = MT5Tokenizer.from_pretrained(model_name)
                self.model = MT5ForConditionalGeneration.from_pretrained(model_name)
            elif "mbart" in model_name.lower():
                self.tokenizer = MBartTokenizer.from_pretrained(model_name)
                self.model = MBartForConditionalGeneration.from_pretrained(model_name)
                # 设置语言代码
                self.tokenizer.src_lang = "en_XX"
                self.tokenizer.tgt_lang = "zh_CN"
            elif "marian" in model_name.lower():
                self.tokenizer = MarianTokenizer.from_pretrained(model_name)
                self.model = MarianMTModel.from_pretrained(model_name)
            else:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            self.model.to(self.device)
            
            # 计算模型参数量
            total_params = sum(p.numel() for p in self.model.parameters())
            trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
            
            logger.info(f"模型已加载到设备: {self.device}")
            logger.info(f"总参数量: {total_params:,}")
            logger.info(f"可训练参数量: {trainable_params:,}")
            
        except Exception as e:
            logger.error(f"模型加载失败: {e}")
            raise
    
    def load_translation_data(self, 
                             pairs_directory: str = "individual_pairs",
                             train_ratio: float = 0.7,
                             val_ratio: float = 0.2,
                             test_ratio: float = 0.1):
        """加载翻译数据并分割"""
        if not os.path.exists(pairs_directory):
            logger.error(f"目录 {pairs_directory} 不存在")
            return
        
        logger.info(f"正在从 {pairs_directory} 加载翻译数据...")
        
        all_examples = []
        
        for filename in os.listdir(pairs_directory):
            if filename.endswith('.json'):
                filepath = os.path.join(pairs_directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if 'english' in data and 'chinese' in data:
                        example = EnhancedTranslationExample(
                            source_text=data['english'],
                            target_text=data['chinese'],
                            domain=self._classify_domain(data['english']),
                            difficulty=self._assess_difficulty(data['english']),
                            quality_score=self._assess_quality(data['english'], data['chinese']),
                            source_file=filename,
                            metadata={
                                'file_size': len(data['english']) + len(data['chinese']),
                                'has_pokemon_terms': self._has_pokemon_terms(data['english']),
                                'sentence_count': len(re.findall(r'[.!?]+', data['english']))
                            }
                        )
                        
                        all_examples.append(example)
                        self._extract_terms(data['english'], data['chinese'])
                        
                except Exception as e:
                    logger.warning(f"加载文件 {filename} 失败: {e}")
                    continue
        
        # 按质量和难度排序
        all_examples.sort(key=lambda x: (x.quality_score, -x.difficulty), reverse=True)
        
        # 分割数据集
        total_count = len(all_examples)
        train_count = int(total_count * train_ratio)
        val_count = int(total_count * val_ratio)
        
        self.training_examples = all_examples[:train_count]
        self.validation_examples = all_examples[train_count:train_count + val_count]
        self.test_examples = all_examples[train_count + val_count:]
        
        # 更新统计信息
        self.learning_stats.update({
            "total_examples": total_count,
            "training_examples": len(self.training_examples),
            "validation_examples": len(self.validation_examples),
            "test_examples": len(self.test_examples)
        })
        
        logger.info(f"数据加载完成:")
        logger.info(f"  总计: {total_count} 个样本")
        logger.info(f"  训练集: {len(self.training_examples)} 个")
        logger.info(f"  验证集: {len(self.validation_examples)} 个")
        logger.info(f"  测试集: {len(self.test_examples)} 个")
        logger.info(f"  术语词典: {sum(len(d) for d in self.term_dictionaries.values())} 个术语")
    
    def _classify_domain(self, text: str) -> str:
        """分类文本领域"""
        if not hasattr(self, 'config') or 'pokemon_domains' not in self.config:
            # 简单分类
            pokemon_keywords = ['pokemon', 'move', 'ability', 'type', 'stat']
            strategy_keywords = ['strategy', 'team', 'synergy', 'counter']
            
            text_lower = text.lower()
            if any(keyword in text_lower for keyword in pokemon_keywords):
                return "pokemon"
            elif any(keyword in text_lower for keyword in strategy_keywords):
                return "strategy"
            else:
                return "general"
        
        # 使用配置文件中的领域分类
        domains = self.config['pokemon_domains']
        text_lower = text.lower()
        
        domain_scores = {}
        for domain_name, domain_info in domains.items():
            score = sum(1 for keyword in domain_info['keywords'] if keyword in text_lower)
            if score > 0:
                domain_scores[domain_name] = score * domain_info['difficulty_weight']
        
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        else:
            return "general"
    
    def _assess_difficulty(self, text: str) -> float:
        """评估文本难度"""
        word_count = len(text.split())
        sentence_count = len(re.findall(r'[.!?]+', text))
        complex_words = len(re.findall(r'\b\w{8,}\b', text))
        technical_terms = len(re.findall(r'\b[A-Z][a-z]+-[A-Z]\b|\bMega \w+\b', text))
        
        # 综合难度评分
        difficulty = min(1.0, (
            word_count / 50 * 0.3 +
            complex_words / 5 * 0.3 +
            technical_terms / 3 * 0.2 +
            sentence_count / 3 * 0.2
        ))
        
        return difficulty
    
    def _assess_quality(self, english: str, chinese: str) -> float:
        """评估翻译质量"""
        en_words = len(english.split())
        cn_chars = len(re.findall(r'[\u4e00-\u9fff]', chinese))
        
        if en_words == 0:
            return 0.0
        
        # 长度比例评分
        length_ratio = cn_chars / en_words
        length_score = min(1.0, length_ratio / 1.5) if length_ratio <= 3.0 else 0.3
        
        # 内容完整性评分
        completeness_score = 1.0 if len(chinese.strip()) > 0 else 0.0
        
        # 中文字符比例评分
        total_chars = len(chinese)
        chinese_ratio = cn_chars / total_chars if total_chars > 0 else 0.0
        chinese_score = min(1.0, chinese_ratio * 1.2)
        
        # 综合质量评分
        quality = (length_score * 0.4 + completeness_score * 0.3 + chinese_score * 0.3)
        
        return quality
    
    def _has_pokemon_terms(self, text: str) -> bool:
        """检查是否包含宝可梦术语"""
        pokemon_patterns = [
            r'\b[A-Z][a-z]+-[A-Z]\b',  # Giratina-O
            r'\bMega [A-Z][a-z]+\b',    # Mega Garchomp
            r'\b(?:HP|Attack|Defense|Speed|Special)\b',  # 属性值
            r'\b(?:Ghost|Dragon|Fire|Water|Grass|Electric)\b'  # 属性类型
        ]
        
        return any(re.search(pattern, text) for pattern in pokemon_patterns)
    
    def _extract_terms(self, english: str, chinese: str):
        """提取专业术语"""
        # 宝可梦名称
        pokemon_patterns = [
            r'\b[A-Z][a-z]+-[A-Z]\b',
            r'\bMega [A-Z][a-z]+\b',
            r'\b[A-Z][a-z]{4,}(?=\s+(?:is|can|has|learns))\b'
        ]
        
        # 招式名称
        move_patterns = [
            r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',
            r'\b[A-Z][a-z]+(?=\s+(?:hits|deals|can))\b'
        ]
        
        # 提取中文术语
        chinese_terms = re.findall(r'[\u4e00-\u9fff]+', chinese)
        
        # 简单的术语对齐（实际应用中需要更复杂的算法）
        for pattern_list, term_type in [(pokemon_patterns, 'pokemon_names'), (move_patterns, 'moves')]:
            for pattern in pattern_list:
                matches = re.findall(pattern, english)
                for i, match in enumerate(matches):
                    if i < len(chinese_terms) and match not in self.term_dictionaries[term_type]:
                        self.term_dictionaries[term_type][match] = chinese_terms[i]
    
    def fine_tune_model(self, 
                       config_name: str = "development",
                       output_dir: str = "./enhanced_fine_tuned_model",
                       custom_config: Dict[str, Any] = None):
        """微调模型"""
        if not self.training_examples:
            logger.error("没有训练数据")
            return None
        
        # 获取训练配置
        if custom_config:
            train_config = TrainingConfig(**custom_config)
        else:
            train_config = TrainingConfig(**self.config["training_configs"][config_name])
        
        logger.info(f"开始微调模型，配置: {train_config.description}")
        start_time = datetime.now()
        
        # 创建数据集
        train_dataset = EnhancedPokemonDataset(
            self.training_examples, 
            self.tokenizer,
            max_length=self.model_config.max_length
        )
        
        eval_dataset = None
        if self.validation_examples:
            eval_dataset = EnhancedPokemonDataset(
                self.validation_examples,
                self.tokenizer,
                max_length=self.model_config.max_length
            )
        
        # 设置训练参数
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=train_config.num_epochs,
            per_device_train_batch_size=self.model_config.recommended_batch_size,
            per_device_eval_batch_size=self.model_config.recommended_batch_size,
            warmup_steps=train_config.warmup_steps,
            weight_decay=0.01,
            logging_dir=f"{output_dir}/logs",
            logging_steps=100,
            save_steps=train_config.save_steps,
            eval_steps=train_config.eval_steps,
            evaluation_strategy="steps" if eval_dataset else "no",
            save_strategy="steps",
            load_best_model_at_end=True if eval_dataset else False,
            metric_for_best_model="eval_loss" if eval_dataset else None,
            learning_rate=train_config.learning_rate,
            fp16=torch.cuda.is_available(),
            dataloader_pin_memory=True,
            remove_unused_columns=False,
            report_to=None,  # 禁用wandb等报告
            save_total_limit=3,  # 只保留最近3个检查点
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
        
        try:
            # 开始训练
            train_result = self.trainer.train()
            
            # 保存模型
            self.trainer.save_model()
            self.tokenizer.save_pretrained(output_dir)
            
            # 更新统计信息
            end_time = datetime.now()
            training_time = (end_time - start_time).total_seconds()
            
            self.learning_stats.update({
                "epochs_trained": train_config.num_epochs,
                "training_time": training_time,
                "last_training_config": asdict(train_config)
            })
            
            logger.info(f"微调完成！训练时间: {training_time:.2f}秒")
            logger.info(f"模型已保存到: {output_dir}")
            
            return train_result
            
        except Exception as e:
            logger.error(f"训练过程中出现错误: {e}")
            raise
    
    def translate_text(self, 
                      text: str, 
                      max_length: int = None,
                      num_beams: int = 4,
                      temperature: float = 1.0,
                      do_sample: bool = False) -> str:
        """翻译文本"""
        if max_length is None:
            max_length = self.model_config.max_length
        
        # 预处理
        processed_text = self._preprocess_text(text)
        
        # 编码
        inputs = self.tokenizer(
            processed_text,
            return_tensors="pt",
            max_length=max_length,
            truncation=True,
            padding=True
        ).to(self.device)
        
        # 生成
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=num_beams,
                temperature=temperature,
                do_sample=do_sample,
                early_stopping=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        # 解码
        translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # 后处理
        final_translation = self._postprocess_translation(translation)
        
        return final_translation
    
    def _preprocess_text(self, text: str) -> str:
        """预处理文本"""
        # 标准化空格
        text = re.sub(r'\s+', ' ', text.strip())
        
        # 应用术语替换（可选）
        if hasattr(self, 'config') and self.config.get('preprocessing', {}).get('term_replacement', {}).get('enable_pokemon_terms', False):
            for en_term, cn_term in self.term_dictionaries['pokemon_names'].items():
                text = re.sub(r'\b' + re.escape(en_term) + r'\b', f"[{en_term}]", text)
        
        return text
    
    def _postprocess_translation(self, translation: str) -> str:
        """后处理翻译"""
        # 应用术语映射
        for term_type, term_dict in self.term_dictionaries.items():
            for en_term, cn_term in term_dict.items():
                # 替换术语标记
                translation = translation.replace(f"[{en_term}]", cn_term)
                # 直接替换（不区分大小写）
                translation = re.sub(
                    r'\b' + re.escape(en_term) + r'\b', 
                    cn_term, 
                    translation, 
                    flags=re.IGNORECASE
                )
        
        return translation.strip()
    
    def comprehensive_evaluate(self, test_examples: List[EnhancedTranslationExample] = None) -> Dict[str, float]:
        """综合评估模型"""
        if test_examples is None:
            test_examples = self.test_examples if self.test_examples else self.validation_examples
        
        if not test_examples:
            logger.warning("没有测试数据")
            return {}
        
        logger.info(f"开始综合评估，测试样本数: {len(test_examples)}")
        
        # 评估指标
        bleu_scores = []
        character_similarities = []
        length_ratios = []
        domain_scores = defaultdict(list)
        
        predictions = []
        references = []
        
        for example in test_examples:
            try:
                predicted = self.translate_text(example.source_text)
                reference = example.target_text
                
                predictions.append(predicted)
                references.append(reference)
                
                # BLEU分数
                bleu = sacrebleu.sentence_bleu(predicted, [reference]).score
                bleu_scores.append(bleu)
                
                # 字符相似度
                char_sim = self._calculate_character_similarity(predicted, reference)
                character_similarities.append(char_sim)
                
                # 长度比例
                len_ratio = len(predicted) / len(reference) if len(reference) > 0 else 0
                length_ratios.append(len_ratio)
                
                # 按领域分组
                domain_scores[example.domain].append(char_sim)
                
            except Exception as e:
                logger.warning(f"评估样本时出错: {e}")
                bleu_scores.append(0.0)
                character_similarities.append(0.0)
                length_ratios.append(0.0)
        
        # 计算整体BLEU
        corpus_bleu = sacrebleu.corpus_bleu(predictions, [references]).score
        
        # 汇总结果
        evaluation_results = {
            "corpus_bleu": corpus_bleu,
            "avg_sentence_bleu": np.mean(bleu_scores) if bleu_scores else 0.0,
            "avg_character_similarity": np.mean(character_similarities) if character_similarities else 0.0,
            "avg_length_ratio": np.mean(length_ratios) if length_ratios else 0.0,
            "bleu_std": np.std(bleu_scores) if bleu_scores else 0.0,
            "char_sim_std": np.std(character_similarities) if character_similarities else 0.0,
            "total_samples": len(test_examples)
        }
        
        # 按领域的评估结果
        for domain, scores in domain_scores.items():
            if scores:
                evaluation_results[f"{domain}_avg_score"] = np.mean(scores)
                evaluation_results[f"{domain}_sample_count"] = len(scores)
        
        # 更新最佳分数
        if "best_scores" not in self.learning_stats:
            self.learning_stats["best_scores"] = {}
        
        current_best = self.learning_stats["best_scores"].get("corpus_bleu", 0.0)
        if corpus_bleu > current_best:
            self.learning_stats["best_scores"]["corpus_bleu"] = corpus_bleu
            self.learning_stats["best_scores"]["timestamp"] = datetime.now().isoformat()
        
        # 记录评估历史
        self.learning_stats["evaluation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "corpus_bleu": corpus_bleu,
            "avg_char_similarity": evaluation_results["avg_character_similarity"],
            "sample_count": len(test_examples)
        })
        
        logger.info(f"评估完成:")
        logger.info(f"  语料库BLEU: {corpus_bleu:.2f}")
        logger.info(f"  平均字符相似度: {evaluation_results['avg_character_similarity']:.3f}")
        logger.info(f"  平均长度比例: {evaluation_results['avg_length_ratio']:.3f}")
        
        return evaluation_results
    
    def _calculate_character_similarity(self, predicted: str, reference: str) -> float:
        """计算字符级相似度"""
        pred_chars = set(predicted)
        ref_chars = set(reference)
        
        if not pred_chars and not ref_chars:
            return 1.0
        
        intersection = len(pred_chars & ref_chars)
        union = len(pred_chars | ref_chars)
        
        return intersection / union if union > 0 else 0.0
    
    def save_comprehensive_report(self, output_path: str = None) -> str:
        """保存综合学习报告"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"enhanced_transformers_report_{timestamp}.json"
        
        # 生成样本统计
        domain_stats = defaultdict(int)
        difficulty_stats = defaultdict(int)
        quality_stats = defaultdict(int)
        
        all_examples = self.training_examples + self.validation_examples + self.test_examples
        
        for example in all_examples:
            domain_stats[example.domain] += 1
            difficulty_stats[f"difficulty_{int(example.difficulty * 10)}"] += 1
            quality_stats[f"quality_{int(example.quality_score * 10)}"] += 1
        
        report = {
            "metadata": {
                "generation_time": datetime.now().isoformat(),
                "model_config": asdict(self.model_config),
                "device_info": str(self.device),
                "total_parameters": sum(p.numel() for p in self.model.parameters()) if self.model else 0
            },
            "data_statistics": {
                "total_examples": len(all_examples),
                "training_examples": len(self.training_examples),
                "validation_examples": len(self.validation_examples),
                "test_examples": len(self.test_examples),
                "domain_distribution": dict(domain_stats),
                "difficulty_distribution": dict(difficulty_stats),
                "quality_distribution": dict(quality_stats)
            },
            "learning_statistics": self.learning_stats,
            "term_dictionaries": {
                term_type: dict(list(term_dict.items())[:50])  # 限制每类术语数量
                for term_type, term_dict in self.term_dictionaries.items()
                if term_dict
            },
            "model_performance": {
                "best_scores": self.learning_stats.get("best_scores", {}),
                "evaluation_history": self.learning_stats.get("evaluation_history", []),
                "training_time_total": self.learning_stats.get("training_time", 0.0)
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"综合学习报告已保存到: {output_path}")
        return output_path

def main():
    """主函数演示"""
    if not TRANSFORMERS_AVAILABLE:
        print("请先安装依赖: pip install transformers torch sacrebleu")
        return
    
    try:
        # 创建增强版学习模块
        module = EnhancedTransformersModule(
            config_path="transformers_config.json",
            model_key="mt5_small"
        )
        
        # 加载数据
        module.load_translation_data()
        
        if module.training_examples:
            # 微调模型
            module.fine_tune_model(config_name="quick_test")
            
            # 综合评估
            results = module.comprehensive_evaluate()
            
            # 保存报告
            module.save_comprehensive_report()
            
            # 测试翻译
            test_text = "Giratina-O is a powerful Ghost/Dragon-type Pokemon with excellent offensive capabilities."
            translation = module.translate_text(test_text)
            print(f"\n测试翻译:")
            print(f"原文: {test_text}")
            print(f"译文: {translation}")
        
        else:
            print("没有找到训练数据")
    
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()