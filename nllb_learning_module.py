# -*- coding: utf-8 -*-
"""
NLLB学习模块
基于Facebook NLLB-200模型的增强版翻译学习系统
支持200+语言的多语言翻译、模型微调和综合评估
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

# NLLB语言代码映射
NLLB_LANGUAGE_CODES = {
    "chinese": "zho_Hans",  # 中文简体
    "english": "eng_Latn",  # 英文
    "japanese": "jpn_Jpan",  # 日文
    "korean": "kor_Hang",   # 韩文
    "french": "fra_Latn",   # 法文
    "german": "deu_Latn",   # 德文
    "spanish": "spa_Latn",  # 西班牙文
    "italian": "ita_Latn",  # 意大利文
    "portuguese": "por_Latn", # 葡萄牙文
    "russian": "rus_Cyrl",  # 俄文
    "arabic": "arb_Arab",   # 阿拉伯文
    "hindi": "hin_Deva",    # 印地文
    "thai": "tha_Thai",     # 泰文
    "vietnamese": "vie_Latn", # 越南文
}

@dataclass
class NLLBTranslationExample:
    """NLLB翻译样本"""
    source_text: str
    target_text: str
    source_lang: str = "english"
    target_lang: str = "chinese"
    domain: str = "general"
    difficulty: float = 1.0
    quality_score: float = 1.0
    source_file: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        # 验证语言代码
        if self.source_lang not in NLLB_LANGUAGE_CODES:
            logger.warning(f"未知源语言: {self.source_lang}, 使用默认英文")
            self.source_lang = "english"
        if self.target_lang not in NLLB_LANGUAGE_CODES:
            logger.warning(f"未知目标语言: {self.target_lang}, 使用默认中文")
            self.target_lang = "chinese"

@dataclass
class NLLBModelConfig:
    """NLLB模型配置"""
    model_name: str = "facebook/nllb-200-distilled-600M"
    max_length: int = 512
    num_beams: int = 4
    temperature: float = 1.0
    do_sample: bool = False
    early_stopping: bool = True
    length_penalty: float = 1.0
    repetition_penalty: float = 1.0
    
class NLLBDataset(Dataset):
    """NLLB数据集类"""
    
    def __init__(self, 
                 examples: List[NLLBTranslationExample], 
                 tokenizer, 
                 max_length: int = 512):
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        example = self.examples[idx]
        
        # 获取NLLB语言代码
        src_lang_code = NLLB_LANGUAGE_CODES[example.source_lang]
        tgt_lang_code = NLLB_LANGUAGE_CODES[example.target_lang]
        
        # 编码源文本
        inputs = self.tokenizer(
            example.source_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        # 编码目标文本
        with self.tokenizer.as_target_tokenizer():
            targets = self.tokenizer(
                example.target_text,
                max_length=self.max_length,
                padding="max_length",
                truncation=True,
                return_tensors="pt"
            )
        
        return {
            "input_ids": inputs["input_ids"].flatten(),
            "attention_mask": inputs["attention_mask"].flatten(),
            "labels": targets["input_ids"].flatten(),
            "source_lang": src_lang_code,
            "target_lang": tgt_lang_code
        }

class NLLBLearningModule:
    """NLLB学习模块主类"""
    
    def __init__(self, config_path: str = "nllb_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.model_config = NLLBModelConfig(**self.config.get("model", {}))
        self.device = self._setup_device()
        self.tokenizer = None
        self.model = None
        self.training_data = []
        self.validation_data = []
        self.test_data = []
        self.learning_stats = {
            "total_examples": 0,
            "domains": defaultdict(int),
            "languages": defaultdict(int),
            "difficulty_distribution": defaultdict(int),
            "quality_distribution": defaultdict(int)
        }
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"配置文件 {self.config_path} 未找到，使用默认配置")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"配置文件格式错误: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "model": {
                "model_name": "facebook/nllb-200-distilled-600M",
                "max_length": 512,
                "num_beams": 4,
                "temperature": 1.0,
                "do_sample": False,
                "early_stopping": True,
                "length_penalty": 1.0,
                "repetition_penalty": 1.0
            },
            "training": {
                "num_epochs": 3,
                "learning_rate": 5e-5,
                "warmup_steps": 500,
                "save_steps": 1000,
                "eval_steps": 500,
                "per_device_train_batch_size": 4,
                "per_device_eval_batch_size": 8,
                "gradient_accumulation_steps": 2
            },
            "data": {
                "train_split": 0.8,
                "val_split": 0.1,
                "test_split": 0.1,
                "min_length": 5,
                "max_length": 512
            },
            "languages": {
                "source": "english",
                "target": "chinese"
            }
        }
    
    def _setup_device(self) -> torch.device:
        """设置计算设备"""
        if torch.cuda.is_available():
            device = torch.device("cuda")
            logger.info(f"使用GPU: {torch.cuda.get_device_name()}")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = torch.device("mps")
            logger.info("使用Apple Silicon GPU (MPS)")
        else:
            device = torch.device("cpu")
            logger.info("使用CPU")
        return device
    
    def initialize_model(self, source_lang: str = "english", target_lang: str = "chinese"):
        """初始化NLLB模型"""
        logger.info(f"初始化NLLB模型: {self.model_config.model_name}")
        
        # 获取语言代码
        src_lang_code = NLLB_LANGUAGE_CODES.get(source_lang, "eng_Latn")
        tgt_lang_code = NLLB_LANGUAGE_CODES.get(target_lang, "zho_Hans")
        
        # 初始化tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_config.model_name,
            src_lang=src_lang_code,
            tgt_lang=tgt_lang_code
        )
        
        # 初始化模型
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_config.model_name
        ).to(self.device)
        
        # 计算模型参数量
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        logger.info(f"模型参数总量: {total_params:,}")
        logger.info(f"可训练参数: {trainable_params:,}")
        logger.info(f"源语言: {source_lang} ({src_lang_code})")
        logger.info(f"目标语言: {target_lang} ({tgt_lang_code})")
    
    def load_translation_data(self, data_dir: str) -> List[NLLBTranslationExample]:
        """加载翻译数据"""
        logger.info(f"从 {data_dir} 加载翻译数据")
        
        examples = []
        if not os.path.exists(data_dir):
            logger.error(f"数据目录不存在: {data_dir}")
            return examples
        
        # 遍历所有JSON文件
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(data_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 处理不同的数据格式
                    if isinstance(data, dict):
                        if 'source' in data and 'target' in data:
                            example = self._create_example_from_dict(data, filename)
                            if example:
                                examples.append(example)
                        elif 'translation_pairs' in data:
                            for pair in data['translation_pairs']:
                                example = self._create_example_from_dict(pair, filename)
                                if example:
                                    examples.append(example)
                    elif isinstance(data, list):
                        for item in data:
                            example = self._create_example_from_dict(item, filename)
                            if example:
                                examples.append(example)
                                
                except Exception as e:
                    logger.error(f"读取文件 {filename} 时出错: {e}")
        
        # 数据质量评估和排序
        examples = self._assess_and_sort_data(examples)
        
        # 数据分割
        self._split_data(examples)
        
        logger.info(f"成功加载 {len(examples)} 个翻译样本")
        logger.info(f"训练集: {len(self.training_data)} 样本")
        logger.info(f"验证集: {len(self.validation_data)} 样本")
        logger.info(f"测试集: {len(self.test_data)} 样本")
        
        return examples
    
    def _create_example_from_dict(self, data: Dict, filename: str) -> Optional[NLLBTranslationExample]:
        """从字典创建翻译样本"""
        try:
            source_text = data.get('source', data.get('english', data.get('en', '')))
            target_text = data.get('target', data.get('chinese', data.get('zh', '')))
            
            if not source_text or not target_text:
                return None
            
            # 检测语言
            source_lang = self._detect_language(source_text)
            target_lang = self._detect_language(target_text)
            
            # 评估难度和质量
            difficulty = self._assess_difficulty(source_text, target_text)
            quality = self._assess_quality(source_text, target_text)
            
            # 分类领域
            domain = self._classify_domain(source_text)
            
            example = NLLBTranslationExample(
                source_text=source_text.strip(),
                target_text=target_text.strip(),
                source_lang=source_lang,
                target_lang=target_lang,
                domain=domain,
                difficulty=difficulty,
                quality_score=quality,
                source_file=filename,
                metadata={
                    'original_data': data,
                    'created_at': datetime.now().isoformat()
                }
            )
            
            # 更新统计信息
            self._update_stats(example)
            
            return example
            
        except Exception as e:
            logger.error(f"创建样本时出错: {e}")
            return None
    
    def _detect_language(self, text: str) -> str:
        """简单的语言检测"""
        # 检测中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        # 检测日文字符
        japanese_chars = len(re.findall(r'[\u3040-\u309f\u30a0-\u30ff]', text))
        # 检测韩文字符
        korean_chars = len(re.findall(r'[\uac00-\ud7af]', text))
        
        total_chars = len(text)
        if total_chars == 0:
            return "english"
        
        if chinese_chars / total_chars > 0.3:
            return "chinese"
        elif japanese_chars / total_chars > 0.3:
            return "japanese"
        elif korean_chars / total_chars > 0.3:
            return "korean"
        else:
            return "english"
    
    def _classify_domain(self, text: str) -> str:
        """分类文本领域"""
        text_lower = text.lower()
        
        # 宝可梦相关关键词
        pokemon_keywords = [
            'pokemon', 'pokémon', 'pikachu', 'charizard', 'blastoise', 'venusaur',
            'gym', 'trainer', 'battle', 'evolution', 'legendary', 'shiny',
            'type', 'move', 'ability', 'stats', 'nature', 'iv', 'ev',
            '宝可梦', '神奇宝贝', '精灵', '训练师', '道馆', '进化', '属性', '技能'
        ]
        
        # 游戏相关关键词
        game_keywords = [
            'game', 'play', 'level', 'score', 'player', 'strategy', 'competitive',
            '游戏', '玩家', '等级', '分数', '策略', '竞技'
        ]
        
        if any(keyword in text_lower for keyword in pokemon_keywords):
            return "pokemon"
        elif any(keyword in text_lower for keyword in game_keywords):
            return "gaming"
        else:
            return "general"
    
    def _assess_difficulty(self, source: str, target: str) -> float:
        """评估翻译难度"""
        # 基于文本长度、复杂度等因素
        source_len = len(source.split())
        target_len = len(target)
        
        # 长度因子
        length_factor = min(source_len / 20, 2.0)
        
        # 复杂词汇因子
        complex_words = len(re.findall(r'\b\w{8,}\b', source))
        complexity_factor = min(complex_words / 5, 2.0)
        
        # 特殊字符因子
        special_chars = len(re.findall(r'[^\w\s]', source))
        special_factor = min(special_chars / 10, 1.5)
        
        difficulty = (length_factor + complexity_factor + special_factor) / 3
        return min(max(difficulty, 0.1), 3.0)
    
    def _assess_quality(self, source: str, target: str) -> float:
        """评估翻译质量"""
        # 基本质量检查
        if not source.strip() or not target.strip():
            return 0.1
        
        # 长度比例检查
        source_len = len(source.split())
        target_len = len(target)
        
        if source_len == 0 or target_len == 0:
            return 0.1
        
        # 合理的长度比例
        length_ratio = target_len / source_len
        if length_ratio < 0.3 or length_ratio > 5.0:
            quality = 0.5
        else:
            quality = 1.0
        
        # 检查是否包含明显错误
        if '???' in target or '###' in target:
            quality *= 0.5
        
        return min(max(quality, 0.1), 1.0)
    
    def _assess_and_sort_data(self, examples: List[NLLBTranslationExample]) -> List[NLLBTranslationExample]:
        """评估和排序数据"""
        # 按质量和难度排序
        examples.sort(key=lambda x: (x.quality_score, -x.difficulty), reverse=True)
        return examples
    
    def _split_data(self, examples: List[NLLBTranslationExample]):
        """分割数据集"""
        total = len(examples)
        train_size = int(total * self.config['data']['train_split'])
        val_size = int(total * self.config['data']['val_split'])
        
        self.training_data = examples[:train_size]
        self.validation_data = examples[train_size:train_size + val_size]
        self.test_data = examples[train_size + val_size:]
    
    def _update_stats(self, example: NLLBTranslationExample):
        """更新学习统计信息"""
        self.learning_stats['total_examples'] += 1
        self.learning_stats['domains'][example.domain] += 1
        self.learning_stats['languages'][f"{example.source_lang}->{example.target_lang}"] += 1
        
        # 难度分布
        difficulty_level = "easy" if example.difficulty < 1.0 else "medium" if example.difficulty < 2.0 else "hard"
        self.learning_stats['difficulty_distribution'][difficulty_level] += 1
        
        # 质量分布
        quality_level = "low" if example.quality_score < 0.5 else "medium" if example.quality_score < 0.8 else "high"
        self.learning_stats['quality_distribution'][quality_level] += 1
    
    def translate_text(self, text: str, source_lang: str = "english", target_lang: str = "chinese") -> str:
        """翻译文本"""
        if not self.model or not self.tokenizer:
            raise ValueError("模型未初始化，请先调用 initialize_model()")
        
        # 获取语言代码
        src_lang_code = NLLB_LANGUAGE_CODES.get(source_lang, "eng_Latn")
        tgt_lang_code = NLLB_LANGUAGE_CODES.get(target_lang, "zho_Hans")
        
        # 编码输入
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        
        # 生成翻译
        with torch.no_grad():
            translated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.lang_code_to_id[tgt_lang_code],
                max_length=self.model_config.max_length,
                num_beams=self.model_config.num_beams,
                temperature=self.model_config.temperature,
                do_sample=self.model_config.do_sample,
                early_stopping=self.model_config.early_stopping,
                length_penalty=self.model_config.length_penalty,
                repetition_penalty=self.model_config.repetition_penalty
            )
        
        # 解码结果
        translated_text = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return translated_text
    
    def fine_tune_model(self, output_dir: str = "./nllb_finetuned"):
        """微调模型"""
        if not self.training_data:
            raise ValueError("没有训练数据，请先加载数据")
        
        logger.info("开始微调NLLB模型")
        
        # 创建数据集
        train_dataset = NLLBDataset(self.training_data, self.tokenizer, self.model_config.max_length)
        val_dataset = NLLBDataset(self.validation_data, self.tokenizer, self.model_config.max_length)
        
        # 数据整理器
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=self.tokenizer,
            model=self.model,
            padding=True
        )
        
        # 训练参数
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=self.config['training']['num_epochs'],
            per_device_train_batch_size=self.config['training']['per_device_train_batch_size'],
            per_device_eval_batch_size=self.config['training']['per_device_eval_batch_size'],
            gradient_accumulation_steps=self.config['training']['gradient_accumulation_steps'],
            learning_rate=self.config['training']['learning_rate'],
            warmup_steps=self.config['training']['warmup_steps'],
            save_steps=self.config['training']['save_steps'],
            eval_steps=self.config['training']['eval_steps'],
            evaluation_strategy="steps",
            save_strategy="steps",
            logging_steps=100,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            report_to=None,
            remove_unused_columns=False
        )
        
        # 创建训练器
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
        )
        
        # 开始训练
        trainer.train()
        
        # 保存模型
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        
        logger.info(f"模型微调完成，保存至: {output_dir}")
    
    def evaluate_model(self) -> Dict[str, Any]:
        """评估模型性能"""
        if not self.test_data:
            logger.warning("没有测试数据")
            return {}
        
        logger.info("开始评估模型")
        
        predictions = []
        references = []
        
        for example in self.test_data[:50]:  # 限制评估样本数量
            try:
                prediction = self.translate_text(
                    example.source_text,
                    example.source_lang,
                    example.target_lang
                )
                predictions.append(prediction)
                references.append(example.target_text)
            except Exception as e:
                logger.error(f"翻译失败: {e}")
                continue
        
        # 计算BLEU分数
        bleu_score = 0.0
        if predictions and references:
            try:
                bleu = sacrebleu.corpus_bleu(predictions, [references])
                bleu_score = bleu.score
            except Exception as e:
                logger.error(f"计算BLEU分数失败: {e}")
        
        evaluation_results = {
            "bleu_score": bleu_score,
            "total_samples": len(self.test_data),
            "evaluated_samples": len(predictions),
            "success_rate": len(predictions) / len(self.test_data) if self.test_data else 0,
            "sample_translations": [
                {
                    "source": self.test_data[i].source_text,
                    "reference": self.test_data[i].target_text,
                    "prediction": predictions[i] if i < len(predictions) else "N/A"
                }
                for i in range(min(5, len(self.test_data)))
            ]
        }
        
        logger.info(f"评估完成 - BLEU分数: {bleu_score:.2f}")
        return evaluation_results
    
    def save_learning_report(self, output_path: str = None) -> str:
        """保存学习报告"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"nllb_learning_report_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "model_config": asdict(self.model_config),
            "training_config": self.config.get('training', {}),
            "learning_statistics": dict(self.learning_stats),
            "data_summary": {
                "total_examples": len(self.training_data) + len(self.validation_data) + len(self.test_data),
                "training_examples": len(self.training_data),
                "validation_examples": len(self.validation_data),
                "test_examples": len(self.test_data)
            },
            "supported_languages": list(NLLB_LANGUAGE_CODES.keys()),
            "evaluation_results": self.evaluate_model() if self.test_data else {}
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"学习报告已保存至: {output_path}")
        return output_path

def main():
    """主函数演示"""
    if not TRANSFORMERS_AVAILABLE:
        print("请安装必要的依赖库")
        return
    
    # 创建学习模块
    nllb_module = NLLBLearningModule()
    
    # 初始化模型
    nllb_module.initialize_model(source_lang="english", target_lang="chinese")
    
    # 加载数据
    data_dir = "individual_pairs"
    if os.path.exists(data_dir):
        nllb_module.load_translation_data(data_dir)
        
        # 微调模型（可选）
        # nllb_module.fine_tune_model()
        
        # 评估模型
        results = nllb_module.evaluate_model()
        print(f"评估结果: {results}")
        
        # 保存报告
        report_path = nllb_module.save_learning_report()
        print(f"报告已保存: {report_path}")
    else:
        print(f"数据目录 {data_dir} 不存在")
    
    # 测试翻译
    test_texts = [
        "Hello, how are you today?",
        "This is a powerful Pokemon with great stats.",
        "The weather is nice today."
    ]
    
    print("\n=== 翻译测试 ===")
    for text in test_texts:
        try:
            translation = nllb_module.translate_text(text, "english", "chinese")
            print(f"原文: {text}")
            print(f"译文: {translation}")
            print("-" * 50)
        except Exception as e:
            print(f"翻译失败: {e}")

if __name__ == "__main__":
    main()