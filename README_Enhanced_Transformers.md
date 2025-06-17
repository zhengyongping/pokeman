# 增强版Transformers学习模块

基于Hugging Face Transformers库重新设计的宝可梦翻译学习模块，支持多种预训练模型、高级评估指标和智能术语管理。

## 🚀 主要特性

### 核心功能
- **多模型支持**: mT5、mBART、MarianMT等主流翻译模型
- **智能数据管理**: 自动数据分割、质量评估、难度分析
- **专业术语提取**: 自动识别和映射宝可梦专业术语
- **综合评估系统**: BLEU、字符相似度、领域特定评估
- **配置化训练**: 灵活的训练参数配置
- **详细报告生成**: 完整的学习过程记录和分析

### 增强特性
- **领域分类**: 自动识别文本所属领域（宝可梦信息、招式特性、对战策略等）
- **质量评分**: 基于多维度指标的翻译质量自动评估
- **难度分析**: 文本复杂度智能评估
- **术语一致性**: 专业术语的统一翻译管理
- **多设备支持**: CPU、CUDA、Apple Silicon自动适配

## 📋 系统要求

### 基础依赖
```bash
pip install transformers torch sacrebleu numpy scipy
```

### 硬件要求
- **最小配置**: 4GB RAM, CPU
- **推荐配置**: 8GB+ RAM, GPU (CUDA/Apple Silicon)
- **高性能配置**: 16GB+ RAM, 专用GPU

### 支持的模型
| 模型类型 | 参数量 | 内存需求 | 推荐用途 |
|---------|--------|----------|----------|
| mT5-small | 300M | 2GB | 开发测试 |
| mT5-base | 580M | 4GB | 生产环境 |
| mT5-large | 1.2B | 8GB | 高质量翻译 |
| mBART-large | 610M | 4GB | 多语言翻译 |
| MarianMT | 变化 | 2-4GB | 特定语言对 |

## 🛠️ 安装和配置

### 1. 环境准备
```bash
# 克隆项目
git clone <repository_url>
cd sctp

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置文件
项目使用 `transformers_config.json` 进行配置管理：

```json
{
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
    "quick_test": {
      "num_epochs": 1,
      "learning_rate": 5e-5,
      "warmup_steps": 100,
      "save_steps": 500,
      "eval_steps": 250,
      "description": "快速测试配置"
    }
  }
}
```

## 📖 使用指南

### 基础使用

```python
from enhanced_transformers_module import EnhancedTransformersModule

# 1. 初始化模块
module = EnhancedTransformersModule(
    config_path="transformers_config.json",
    model_key="mt5_small",
    device="auto"
)

# 2. 加载翻译数据
module.load_translation_data(
    pairs_directory="individual_pairs",
    train_ratio=0.7,
    val_ratio=0.2,
    test_ratio=0.1
)

# 3. 查看数据统计
print(f"训练集: {len(module.training_examples)} 个样本")
print(f"验证集: {len(module.validation_examples)} 个样本")
print(f"测试集: {len(module.test_examples)} 个样本")

# 4. 测试基础翻译
text = "Giratina-O is a powerful Ghost/Dragon-type Pokemon."
translation = module.translate_text(text)
print(f"原文: {text}")
print(f"译文: {translation}")
```

### 模型微调

```python
# 使用预设配置微调
train_result = module.fine_tune_model(
    config_name="development",
    output_dir="./fine_tuned_model"
)

# 使用自定义配置微调
custom_config = {
    "num_epochs": 3,
    "learning_rate": 3e-5,
    "warmup_steps": 500,
    "save_steps": 1000,
    "eval_steps": 500,
    "description": "自定义配置"
}

train_result = module.fine_tune_model(
    custom_config=custom_config,
    output_dir="./custom_fine_tuned_model"
)
```

### 模型评估

```python
# 综合评估
evaluation_results = module.comprehensive_evaluate()

print(f"语料库BLEU分数: {evaluation_results['corpus_bleu']:.2f}")
print(f"平均字符相似度: {evaluation_results['avg_character_similarity']:.3f}")
print(f"平均长度比例: {evaluation_results['avg_length_ratio']:.3f}")

# 按领域查看评估结果
for key, value in evaluation_results.items():
    if key.endswith('_avg_score'):
        domain = key.replace('_avg_score', '')
        print(f"{domain}领域平均分数: {value:.3f}")
```

### 高级翻译选项

```python
# 不同的翻译参数
translations = {
    "贪婪搜索": module.translate_text(text, num_beams=1),
    "束搜索": module.translate_text(text, num_beams=4),
    "采样": module.translate_text(text, do_sample=True, temperature=0.8),
    "高质量": module.translate_text(text, num_beams=8, max_length=1024)
}

for method, result in translations.items():
    print(f"{method}: {result}")
```

### 术语管理

```python
# 查看提取的术语
for term_type, terms in module.term_dictionaries.items():
    if terms:
        print(f"\n{term_type} ({len(terms)} 个术语):")
        for en, cn in list(terms.items())[:5]:  # 显示前5个
            print(f"  {en} -> {cn}")

# 手动添加术语
module.term_dictionaries['pokemon_names']['Arceus'] = '阿尔宙斯'
module.term_dictionaries['moves']['Judgment'] = '制裁光砾'
```

### 生成学习报告

```python
# 保存综合报告
report_path = module.save_comprehensive_report()
print(f"学习报告已保存到: {report_path}")

# 报告包含的信息：
# - 模型配置和参数统计
# - 数据分布和质量分析
# - 训练过程和性能指标
# - 术语词典和映射关系
# - 评估历史和最佳分数
```

## 🎯 演示脚本

项目提供了完整的演示脚本：

```bash
# 运行基础演示
python demo_enhanced_transformers.py

# 演示内容包括：
# 1. 基本使用方法
# 2. 模型微调过程
# 3. 综合评估系统
# 4. 高级功能展示
# 5. 模型比较分析
```

演示脚本会自动：
- 创建演示数据
- 展示各种功能
- 生成学习报告
- 保存微调模型

## 📊 数据格式

### 输入数据格式
翻译对文件应为JSON格式：

```json
{
  "english": "Giratina-O is a powerful Ghost/Dragon-type Pokemon.",
  "chinese": "骑拉帝纳-起源形态是一只强大的幽灵/龙属性宝可梦。"
}
```

### 数据目录结构
```
individual_pairs/
├── pair_001.json
├── pair_002.json
├── ...
└── pair_n.json
```

### 增强数据结构
系统会自动为每个样本添加元数据：

```python
class EnhancedTranslationExample:
    source_text: str          # 英文原文
    target_text: str          # 中文译文
    domain: str              # 领域分类
    difficulty: float        # 难度评分 (0-1)
    quality_score: float     # 质量评分 (0-1)
    source_file: str         # 来源文件
    metadata: Dict[str, Any] # 额外元数据
```

## 🔧 配置选项

### 模型配置
- `name`: Hugging Face模型名称
- `description`: 模型描述
- `parameters`: 参数量
- `memory_requirement`: 内存需求
- `recommended_batch_size`: 推荐批处理大小
- `max_length`: 最大序列长度
- `languages`: 支持的语言
- `use_case`: 使用场景

### 训练配置
- `num_epochs`: 训练轮数
- `learning_rate`: 学习率
- `warmup_steps`: 预热步数
- `save_steps`: 保存间隔
- `eval_steps`: 评估间隔
- `description`: 配置描述

### 领域配置
- `keywords`: 领域关键词
- `difficulty_weight`: 难度权重
- `description`: 领域描述

## 📈 评估指标

### 自动评估指标
1. **BLEU分数**: 语料库级别和句子级别
2. **字符相似度**: 基于字符集合的Jaccard相似度
3. **长度比例**: 译文与原文的长度比例
4. **领域特定评估**: 按不同领域分组的评估结果

### 质量评估维度
1. **长度合理性**: 译文长度与原文的匹配度
2. **内容完整性**: 译文是否包含完整信息
3. **中文字符比例**: 译文中中文字符的占比
4. **术语一致性**: 专业术语翻译的一致性

## 🚨 注意事项

### 性能优化
1. **内存管理**: 根据可用内存选择合适的模型和批处理大小
2. **设备选择**: 优先使用GPU加速训练和推理
3. **数据预处理**: 合理设置最大序列长度避免截断
4. **检查点保存**: 定期保存模型避免训练中断

### 常见问题
1. **CUDA内存不足**: 减小批处理大小或使用更小的模型
2. **训练速度慢**: 检查设备配置，考虑使用混合精度训练
3. **翻译质量差**: 增加训练数据量，调整学习率和训练轮数
4. **术语翻译不准确**: 手动添加术语映射，提高术语提取精度

### 最佳实践
1. **数据质量**: 确保翻译对的质量和一致性
2. **领域平衡**: 保持不同领域数据的平衡分布
3. **渐进训练**: 从小模型开始，逐步使用更大的模型
4. **定期评估**: 在训练过程中定期评估模型性能
5. **术语维护**: 持续更新和完善术语词典

## 📝 更新日志

### v2.0.0 (当前版本)
- 重新设计基于Transformers库的学习模块
- 添加多模型支持和配置化管理
- 实现智能术语提取和映射
- 增强评估系统和报告生成
- 优化数据处理和质量评估

### 计划功能
- [ ] 支持更多翻译模型
- [ ] 实现在线学习和增量训练
- [ ] 添加Web界面和API服务
- [ ] 集成更多评估指标
- [ ] 支持多语言翻译

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目：

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

---

**注意**: 本项目专注于宝可梦相关内容的英中翻译，术语和评估标准针对该领域进行了优化。如需用于其他领域，请相应调整配置和评估标准。