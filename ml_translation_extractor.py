#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器学习翻译对提取程序
从scraped_threads目录中的文件提取英文原文-中文译文对
支持两种文件格式：
1. 基础格式：包含[SET]和[SET COMMENTS]部分
2. 扩展格式：额外包含[OVERVIEW]和[STRATEGY COMMENTS]部分
"""

import os
import re
import json
import argparse
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TranslationPair:
    """翻译对数据结构"""
    english: str
    chinese: str
    section_type: str  # 'SET_COMMENTS', 'OVERVIEW', 'STRATEGY_COMMENTS'
    source_file: str
    confidence: float = 1.0

class MLTranslationExtractor:
    """机器学习翻译对提取器"""
    
    def __init__(self, scraped_dir: str = "scraped_threads"):
        self.scraped_dir = scraped_dir
        self.translation_pairs: List[TranslationPair] = []
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'failed_files': 0,
            'total_pairs': 0,
            'set_comments_pairs': 0,
            'overview_pairs': 0,
            'strategy_comments_pairs': 0
        }
    
    def extract_all_files(self) -> None:
        """处理scraped_threads目录下的所有文件"""
        if not os.path.exists(self.scraped_dir):
            print(f"错误：目录 {self.scraped_dir} 不存在")
            return
        
        files = [f for f in os.listdir(self.scraped_dir) if f.endswith('.txt')]
        self.stats['total_files'] = len(files)
        
        print(f"开始处理 {len(files)} 个文件...")
        
        for filename in files:
            filepath = os.path.join(self.scraped_dir, filename)
            try:
                self._process_file(filepath, filename)
                self.stats['processed_files'] += 1
                print(f"✓ 处理完成: {filename}")
            except Exception as e:
                self.stats['failed_files'] += 1
                print(f"✗ 处理失败: {filename} - {str(e)}")
        
        self._update_stats()
        self._print_summary()
    
    def _process_file(self, filepath: str, filename: str) -> None:
        """处理单个文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按分割线分割中文翻译和英文原文
        separator = "=" * 80 + "\nORIGINAL THREAD FIRST POST\n" + "=" * 80
        if separator in content:
            parts = content.split(separator)
        else:
            # 尝试其他分割线格式
            alt_separator = "=" * 80
            if alt_separator in content:
                parts = content.split(alt_separator)
                # 过滤掉只包含"ORIGINAL THREAD FIRST POST"的部分
                parts = [part for part in parts if "ORIGINAL THREAD FIRST POST" not in part or len(part.strip()) > 50]
            else:
                print(f"警告：{filename} 没有找到分割线，跳过处理")
                return
        
        if len(parts) < 2:
            print(f"警告：{filename} 分割后部分不足，跳过处理")
            return
        
        chinese_part = parts[0].strip()
        english_part = parts[1].strip() if len(parts) > 1 else ""
        
        # 提取翻译对
        self._extract_translation_pairs(chinese_part, english_part, filename)
    
    def _extract_translation_pairs(self, chinese_part: str, english_part: str, filename: str) -> None:
        """从中文和英文部分提取翻译对"""
        # 1. 提取SET COMMENTS部分
        self._extract_set_comments(chinese_part, english_part, filename)
        
        # 2. 提取OVERVIEW部分（如果存在）
        self._extract_overview(chinese_part, english_part, filename)
        
        # 3. 提取STRATEGY COMMENTS部分（如果存在）
        self._extract_strategy_comments(chinese_part, english_part, filename)
    
    def _extract_set_comments(self, chinese_part: str, english_part: str, filename: str) -> None:
        """提取SET COMMENTS部分的翻译对"""
        # 提取中文SET COMMENTS
        chinese_set_comments = self._find_section(chinese_part, r'\[SET COMMENTS\]', r'\[SET CREDITS\]')
        if not chinese_set_comments:
            return
        
        # 提取英文SET COMMENTS
        english_set_comments = self._find_section(english_part, r'\[SET COMMENTS\]', r'\[SET CREDITS\]')
        if not english_set_comments:
            return
        
        # 清理Chinese Set部分（忽略配置信息）
        chinese_cleaned = self._clean_chinese_set_comments(chinese_set_comments)
        english_cleaned = self._clean_english_text(english_set_comments)
        
        if chinese_cleaned and english_cleaned:
            pair = TranslationPair(
                english=english_cleaned,
                chinese=chinese_cleaned,
                section_type='SET_COMMENTS',
                source_file=filename
            )
            self.translation_pairs.append(pair)
            self.stats['set_comments_pairs'] += 1
    
    def _extract_overview(self, chinese_part: str, english_part: str, filename: str) -> None:
        """提取OVERVIEW部分的翻译对"""
        # 提取中文OVERVIEW
        chinese_overview = self._find_section(chinese_part, r'\[OVERVIEW\]', r'\[SET\]')
        if not chinese_overview:
            return
        
        # 提取英文OVERVIEW
        english_overview = self._find_section(english_part, r'\[OVERVIEW\]', r'\[SET\]')
        if not english_overview:
            return
        
        chinese_cleaned = self._clean_chinese_text(chinese_overview)
        english_cleaned = self._clean_english_text(english_overview)
        
        if chinese_cleaned and english_cleaned:
            pair = TranslationPair(
                english=english_cleaned,
                chinese=chinese_cleaned,
                section_type='OVERVIEW',
                source_file=filename
            )
            self.translation_pairs.append(pair)
            self.stats['overview_pairs'] += 1
    
    def _extract_strategy_comments(self, chinese_part: str, english_part: str, filename: str) -> None:
        """提取STRATEGY COMMENTS部分的翻译对"""
        # 提取中文STRATEGY COMMENTS
        chinese_strategy = self._find_section(chinese_part, r'\[STRATEGY COMMENTS\]', r'\[SET CREDITS\]')
        if not chinese_strategy:
            return
        
        # 提取英文STRATEGY COMMENTS
        english_strategy = self._find_section(english_part, r'\[STRATEGY COMMENTS\]', r'\[SET CREDITS\]')
        if not english_strategy:
            return
        
        # 分别处理Other Options和Checks and Counters部分
        self._extract_strategy_subsections(chinese_strategy, english_strategy, filename)
    
    def _extract_strategy_subsections(self, chinese_strategy: str, english_strategy: str, filename: str) -> None:
        """提取STRATEGY COMMENTS的子部分"""
        # Other Options部分
        chinese_other = self._find_subsection(chinese_strategy, r'Other Options', r'Checks and Counters')
        english_other = self._find_subsection(english_strategy, r'Other Options', r'Checks and Counters')
        
        if chinese_other and english_other:
            chinese_cleaned = self._clean_chinese_text(chinese_other)
            english_cleaned = self._clean_english_text(english_other)
            
            if chinese_cleaned and english_cleaned:
                pair = TranslationPair(
                    english=english_cleaned,
                    chinese=chinese_cleaned,
                    section_type='STRATEGY_COMMENTS_OTHER',
                    source_file=filename
                )
                self.translation_pairs.append(pair)
                self.stats['strategy_comments_pairs'] += 1
        
        # Checks and Counters部分
        chinese_checks = self._find_subsection(chinese_strategy, r'Checks and Counters', None)
        english_checks = self._find_subsection(english_strategy, r'Checks and Counters', None)
        
        if chinese_checks and english_checks:
            chinese_cleaned = self._clean_chinese_text(chinese_checks)
            english_cleaned = self._clean_english_text(english_checks)
            
            if chinese_cleaned and english_cleaned:
                pair = TranslationPair(
                    english=english_cleaned,
                    chinese=chinese_cleaned,
                    section_type='STRATEGY_COMMENTS_CHECKS',
                    source_file=filename
                )
                self.translation_pairs.append(pair)
                self.stats['strategy_comments_pairs'] += 1
    
    def _find_section(self, text: str, start_pattern: str, end_pattern: str) -> Optional[str]:
        """查找指定的文本段落"""
        start_match = re.search(start_pattern, text)
        if not start_match:
            return None
        
        start_pos = start_match.end()
        
        if end_pattern:
            end_match = re.search(end_pattern, text[start_pos:])
            if end_match:
                end_pos = start_pos + end_match.start()
                return text[start_pos:end_pos].strip()
        
        return text[start_pos:].strip()
    
    def _find_subsection(self, text: str, start_marker: str, end_marker: Optional[str]) -> Optional[str]:
        """查找子段落"""
        start_pattern = f'{start_marker}\s*={4,}'
        start_match = re.search(start_pattern, text)
        if not start_match:
            return None
        
        start_pos = start_match.end()
        
        if end_marker:
            end_pattern = f'{end_marker}\s*={4,}'
            end_match = re.search(end_pattern, text[start_pos:])
            if end_match:
                end_pos = start_pos + end_match.start()
                return text[start_pos:end_pos].strip()
        
        return text[start_pos:].strip()
    
    def _clean_chinese_set_comments(self, text: str) -> str:
        """清理中文SET COMMENTS，移除Chinese Set配置信息"""
        # 移除Chinese Set配置行
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # 跳过Chinese Set配置行（包含||分隔符的完整配置行）
            if (line.startswith('Chinese set:') or line.startswith('Chinese Set:') or 
                line.startswith('Chinese set：') or line.startswith('Chinese Set：')):
                continue
            # 跳过包含||分隔符的配置行（这通常是宝可梦配置信息）
            if '||' in line and ('道具：' in line or '特性：' in line or '努力值：' in line or '性格：' in line or '招式：' in line):
                continue
            if line and not self._is_config_line(line):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
    
    def _clean_chinese_text(self, text: str) -> str:
        """清理中文文本"""
        # 移除多余的空行和空白字符
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    def _clean_english_text(self, text: str) -> str:
        """清理英文文本"""
        # 移除多余的空行和空白字符
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    def _is_config_line(self, line: str) -> bool:
        """判断是否为配置行（需要忽略的行）"""
        config_patterns = [
            r'^[A-Za-z\s-]+@[A-Za-z\s-]+$',  # 道具配置
            r'^Ability:',  # 特性
            r'^Tera Type:',  # 太晶属性
            r'^EVs:',  # 努力值
            r'^Nature',  # 性格
            r'^-\s+[A-Za-z\s]+$',  # 招式列表
            r'^\d+\s*(HP|Atk|Def|SpA|SpD|Spe)',  # 努力值分配
        ]
        
        for pattern in config_patterns:
            if re.match(pattern, line):
                return True
        return False
    
    def _update_stats(self) -> None:
        """更新统计信息"""
        self.stats['total_pairs'] = len(self.translation_pairs)
    
    def _print_summary(self) -> None:
        """打印处理摘要"""
        print("\n" + "=" * 60)
        print("处理摘要")
        print("=" * 60)
        print(f"总文件数: {self.stats['total_files']}")
        print(f"成功处理: {self.stats['processed_files']}")
        print(f"处理失败: {self.stats['failed_files']}")
        print(f"\n翻译对统计:")
        print(f"  总翻译对数: {self.stats['total_pairs']}")
        print(f"  SET COMMENTS: {self.stats['set_comments_pairs']}")
        print(f"  OVERVIEW: {self.stats['overview_pairs']}")
        print(f"  STRATEGY COMMENTS: {self.stats['strategy_comments_pairs']}")
        
        if self.stats['total_pairs'] > 0:
            print(f"\n平均每文件翻译对数: {self.stats['total_pairs'] / max(1, self.stats['processed_files']):.1f}")
    
    def save_to_json(self, output_file: str = "ml_translation_pairs.json") -> None:
        """保存翻译对到JSON文件"""
        data = {
            'metadata': {
                'total_pairs': len(self.translation_pairs),
                'extraction_stats': self.stats,
                'description': '从Smogon论坛爬取文件中提取的英文-中文翻译对，用于机器学习训练'
            },
            'translation_pairs': [
                {
                    'english': pair.english,
                    'chinese': pair.chinese,
                    'section_type': pair.section_type,
                    'source_file': pair.source_file,
                    'confidence': pair.confidence
                }
                for pair in self.translation_pairs
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n翻译对已保存到: {output_file}")
    
    def save_to_csv(self, output_file: str = "ml_translation_pairs.csv") -> None:
        """保存翻译对到CSV文件"""
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['英文原文', '中文翻译', '段落类型', '来源文件', '置信度'])
            
            for pair in self.translation_pairs:
                writer.writerow([
                    pair.english.replace('\n', ' '),
                    pair.chinese.replace('\n', ' '),
                    pair.section_type,
                    pair.source_file,
                    pair.confidence
                ])
        
        print(f"翻译对已保存到: {output_file}")
    
    def print_sample_pairs(self, num_samples: int = 3) -> None:
        """打印样本翻译对"""
        if not self.translation_pairs:
            print("没有找到翻译对")
            return
        
        print(f"\n样本翻译对 (显示前{min(num_samples, len(self.translation_pairs))}个):")
        print("=" * 80)
        
        for i, pair in enumerate(self.translation_pairs[:num_samples], 1):
            print(f"\n样本 {i} [{pair.section_type}] - {pair.source_file}:")
            print(f"英文: {pair.english[:200]}{'...' if len(pair.english) > 200 else ''}")
            print(f"中文: {pair.chinese[:200]}{'...' if len(pair.chinese) > 200 else ''}")
            print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description='机器学习翻译对提取程序')
    parser.add_argument('--input-dir', default='scraped_threads', help='输入目录路径')
    parser.add_argument('--output-json', default='ml_translation_pairs.json', help='JSON输出文件名')
    parser.add_argument('--output-csv', default='ml_translation_pairs.csv', help='CSV输出文件名')
    parser.add_argument('--samples', type=int, default=3, help='显示的样本数量')
    parser.add_argument('--no-csv', action='store_true', help='不生成CSV文件')
    
    args = parser.parse_args()
    
    # 创建提取器
    extractor = MLTranslationExtractor(args.input_dir)
    
    # 提取翻译对
    extractor.extract_all_files()
    
    # 显示样本
    extractor.print_sample_pairs(args.samples)
    
    # 保存结果
    extractor.save_to_json(args.output_json)
    if not args.no_csv:
        extractor.save_to_csv(args.output_csv)
    
    print("\n提取完成！")

if __name__ == '__main__':
    main()