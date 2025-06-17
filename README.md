# 英译中个性化翻译程序

一个能够学习用户翻译风格并生成个性化翻译结果的英译中翻译程序。

## 项目特性

### 核心功能

1. **基础翻译功能**
   - 准确翻译输入的英文文本到中文
   - 支持常见的词汇和句式结构

2. **学习与模仿机制**
   - 用户可以提供成对的"英文原文 - 用户期望的中文译文"作为学习样本
   - 程序分析样本，提取翻译风格、语法偏好和特定规范
   - 学习模型持续迭代，随着样本增加，翻译风格更加贴近用户期望

3. **个性化翻译引擎**
   - 基于学习到的风格、语法和规范生成个性化翻译
   - 内置宝可梦领域专业术语支持
   - 智能匹配相似翻译样本作为参考

### 功能特点

- **智能翻译学习**: 从用户输入中学习翻译模式和风格偏好
- **上下文感知**: 根据语境调整翻译策略
- **个性化适应**: 记住用户的翻译习惯和专业术语偏好
- **多格式支持**: 支持JSON、CSV、TXT、XLSX等多种数据保存格式
- **SET格式识别**: 专门识别和提取[SET]至[SET COMMENTS]格式的翻译对照
- **智能配对算法**: 基于相似度计算的智能翻译对配对

### 技术特点

- **风格学习**: 自动识别正式/非正式用词风格
- **语法分析**: 学习句子拆分偏好和被动语态使用习惯
- **术语管理**: 专业术语统一翻译（特别是宝可梦相关术语）
- **数据持久化**: 自动保存学习样本和风格模式
- **相似度匹配**: 基于词汇重叠度查找相似翻译样本
- **网页爬虫**: 自动从Smogon论坛爬取专业翻译对照
- **多种学习模式**: 支持手动学习和自动爬取学习

## 安装和使用

### 环境要求

- Python 3.6+
- 无需额外依赖包（使用Python标准库）

### 快速开始

1. **克隆或下载项目文件**
   ```bash
   # 确保translator.py文件在当前目录
   ```

2. **运行程序**
   ```bash
   python translator.py --help
   ```

### 使用方法

#### 1. 交互模式（推荐）

```bash
python translator.py --interactive
```

在交互模式下，你可以：
- 输入英文文本进行翻译
- 输入 `learn` 进入学习模式
- 输入 `progress` 查看学习进度
- 输入 `quit` 退出程序

#### 2. 学习模式

```bash
python translator.py --learn
```

手动添加翻译样本，程序会学习你的翻译风格。

#### 2.1 从Smogon论坛学习

```bash
python translator.py --learn-smogon
```

自动从Smogon中文翻译存档爬取翻译对照，快速学习专业的宝可梦翻译风格。

添加翻译样本来训练个性化风格：
```
英文原文: Hello, how are you?
期望译文: 你好，你怎么样？
```

#### 3. 直接翻译

```bash
python translator.py --translate "Hello world"
```

#### 4. 显示学习进度

```bash
python translator.py --progress
```

#### 5. 爬虫演示程序

```bash
python demo_scraper.py
```

运行专门的爬虫演示程序，可以选择:
- 集成爬虫演示：直接将爬取的内容集成到翻译器
- 手动爬虫演示：独立运行爬虫并保存结果

## 爬虫演示程序

### 基础爬虫演示
运行爬虫演示：
```bash
python demo_scraper.py
```

该程序提供两种演示模式：
- **集成演示**：展示如何在翻译器中集成爬虫功能
- **手动演示**：展示独立的爬虫功能和数据处理

### 保存功能演示
运行保存功能演示：
```bash
python demo_save_features.py
```

该程序展示改进后的本地保存功能：
- **多格式保存**：JSON、CSV、TXT、Excel格式
- **统计分析**：数据长度、来源分布、类型统计
- **文件管理**：自动目录创建、文件大小显示
- **自定义路径**：支持自定义保存位置

### 高级爬虫选项
使用命令行参数运行爬虫：
```bash
# 从Smogon论坛学习翻译对照（包含SET格式提取）
python translator.py --learn-smogon

# 直接运行爬虫并保存为JSON格式（包含SET格式识别）
python smogon_scraper.py

# 保存为CSV格式
python smogon_scraper.py --format csv

# 保存所有格式
python smogon_scraper.py --save-all-formats

# 自定义输出文件名
python smogon_scraper.py --output my_translations --format xlsx

# 自动加载到翻译器
python smogon_scraper.py --load-to-translator

# 指定爬取URL（默认包含prefix_id=484）
python smogon_scraper.py --url "https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/?prefix_id=484"

# 测试SET格式提取功能
python test_set_extraction.py

# 演示改进后的爬虫功能
python demo_improved_scraper.py
```

## SET格式翻译对提取功能

### 新增功能特性

本项目新增了专门针对Smogon论坛[SET]格式的翻译对提取功能：

- **SET格式识别**: 自动识别[SET]至[SET COMMENTS]格式的内容块
- **智能配对算法**: 基于相似度计算的智能翻译对配对
- **多种配对策略**: 支持按行数配对和基于内容相似度的智能配对
- **精确定位**: 使用prefix_id=484精确定位中文翻译内容
- **统计分析**: 提供详细的配对类型和数据统计
- **同源配对**: 从同一个帖子中提取英文和中文SET，根据内容相似性进行配对

### SET格式翻译对提取功能

本项目新增了对Smogon论坛中[SET]格式内容的智能提取和配对功能：

#### 新增特性
- **智能SET识别**: 自动识别帖子中的[SET]到[SET COMMENTS]格式内容
- **语言分离**: 智能区分英文和中文SET块
- **内容配对**: 根据宝可梦名称、技能数量、努力值等关键信息进行智能配对
- **匹配评分**: 为每个配对计算匹配度分数，确保配对准确性
- **同源配对**: 从同一个帖子中提取英文和中文SET，根据内容相似性进行配对

#### 配对算法特点
- **宝可梦名称匹配**: 内置宝可梦中英文名称映射，权重40%
- **技能数量匹配**: 比较英文和中文SET的技能数量相似度，权重30%
- **数值匹配**: 比较努力值等数字信息的重叠度，权重30%
- **阈值过滤**: 只保留匹配度超过0.5的配对结果

#### 使用示例
```bash
# 使用新的SET格式提取功能
python3 smogon_scraper.py --url "https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/?prefix_id=484"

# 测试SET配对算法
python3 test_set_algorithm.py

# 测试SET配对功能
python3 test_set_pairing.py
```

#### 测试结果
算法测试显示，SET配对功能能够：
- 正确识别和提取SET块
- 准确区分英文和中文内容
- 基于内容相似性进行智能配对
- 达到1.0的匹配度分数（完全匹配的情况下）

### SET格式示例

```
[SET]
Pokemon: Garchomp
Ability: Rough Skin
Level: 50
EVs: 4 HP / 252 Atk / 252 Spe
Nature: Jolly
Item: Choice Scarf
- Dragon Claw
- Earthquake
- Stone Edge
- U-turn
[SET COMMENTS]
This set focuses on speed and attack...
```

对应的中文翻译：
```
[SET]
宝可梦：烈咬陆鲨
特性：粗糙皮肤
等级：50
努力值：4 HP / 252 攻击 / 252 速度
性格：爽朗
道具：讲究围巾
- 龙爪
- 地震
- 尖石攻击
- 急速折返
[SET COMMENTS]
这个配置专注于速度和攻击力...
```

### 使用方法

1. **测试SET格式提取**:
   ```bash
   python test_set_extraction.py
   ```

2. **演示改进功能**:
   ```bash
   python demo_improved_scraper.py
   ```

3. **直接爬取并提取SET格式**:
   ```bash
   python smogon_scraper.py
   ```

## 功能演示

### 基础翻译示例

```
输入: Hello world
基础翻译: 你好世界
个性化翻译: 你好世界
```

### 宝可梦术语翻译

```
输入: The pokemon trainer caught a legendary pokemon
基础翻译: [the]宝可梦训练师[caught][a]传说宝可梦
个性化翻译: 宝可梦训练师捕获了传说宝可梦
```

### 学习样本影响

添加学习样本后：
```
学习样本: "Good morning" -> "早上好"

输入: Good morning everyone
个性化翻译: 早上好[everyone] (参考学习样本: 早上好)
```

## 数据存储

程序会自动创建 `translation_data.json` 文件来保存：
- 用户提供的翻译样本
- 学习到的风格模式
- 语法偏好设置

## 内置宝可梦术语词典

| 英文 | 中文 |
|------|------|
| pokemon | 宝可梦 |
| trainer | 训练师 |
| gym | 道馆 |
| badge | 徽章 |
| evolution | 进化 |
| legendary | 传说 |
| shiny | 异色 |
| pokeball | 精灵球 |
| battle | 对战 |
| champion | 冠军 |

## 学习机制说明

### 风格分析

1. **正式/非正式用词检测**
   - 正式词汇：therefore, furthermore, consequently, nevertheless
   - 非正式词汇：gonna, wanna, yeah, ok, cool

2. **语法偏好学习**
   - 句子拆分倾向：比较英文和中文句子数量
   - 被动语态频率：统计被动语态使用情况

3. **相似度匹配**
   - 基于词汇重叠度计算相似性
   - 阈值设定为30%以上才认为相似

## 扩展建议

为了获得更好的翻译效果，建议：

1. **集成专业翻译API**
   - Google Translate API
   - 百度翻译API
   - 有道翻译API

2. **使用神经机器翻译模型**
   - Transformers库
   - 预训练的中英翻译模型

3. **增强自然语言处理**
   - NLTK用于英文处理
   - jieba用于中文分词

## 注意事项

- 当前版本使用简化的词典翻译，实际效果有限
- 建议提供足够的学习样本以获得更好的个性化效果
- 程序会自动保存数据，请确保有写入权限

## 许可证

本项目仅供学习和研究使用。