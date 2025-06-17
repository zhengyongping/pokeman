#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smogon论坛翻译内容爬虫程序
专门用于从Smogon中文翻译存档中提取原文和翻译对照
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from typing import List, Dict, Tuple
from urllib.parse import urljoin, urlparse
import os

class SmogonScraper:
    def __init__(self, base_url="https://www.smogon.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.translation_pairs = []
        self.processed_urls = set()
        
    def scrape_chinese_archive(self, archive_url="https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/"):
        """爬取中文SV分析存档页面，保存每个thread的第一个回复为txt文件"""
        print(f"开始爬取Smogon中文翻译存档: {archive_url}")
        
        # 创建保存目录
        save_dir = "scraped_threads"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        try:
            # 获取存档页面
            response = self.session.get(archive_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找所有帖子链接
            thread_links = self._extract_thread_links(soup)
            print(f"找到 {len(thread_links)} 个帖子")
            
            # 处理每个帖子
            for i, thread_url in enumerate(thread_links):
                if thread_url in self.processed_urls:
                    continue
                    
                print(f"\n处理第 {i+1}/{len(thread_links)} 个帖子...")
                print(f"URL: {thread_url}")
                
                self._scrape_thread_to_file(thread_url, save_dir)
                self.processed_urls.add(thread_url)
                
                # 添加延迟避免被封
                time.sleep(2)
                
            print(f"\n爬取完成！所有文件已保存到 {save_dir} 目录")
            
        except Exception as e:
            print(f"爬取存档页面时出错: {e}")
            
    def _extract_thread_links(self, soup: BeautifulSoup) -> List[str]:
        """从论坛页面提取帖子链接"""
        thread_links = []
        
        # 查找帖子标题链接
        for link in soup.find_all('a', {'data-tp-primary': 'on'}):
            href = link.get('href')
            if href and '/threads/' in href:
                full_url = urljoin(self.base_url, href)
                thread_links.append(full_url)
                
        # 如果上面的方法没找到，尝试其他选择器
        if not thread_links:
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and '/threads/' in href and 'chinese' in href.lower():
                    full_url = urljoin(self.base_url, href)
                    thread_links.append(full_url)
                    
        return list(set(thread_links))  # 去重
        
    def _scrape_thread_to_file(self, thread_url: str, save_dir: str):
        """爬取单个帖子的主帖（first post）并保存为txt文件"""
        try:
            response = self.session.get(thread_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 获取帖子标题
            title_elem = soup.find('h1', class_='p-title-value')
            title = title_elem.get_text(strip=True) if title_elem else "未知标题"
            print(f"帖子标题: {title}")
            
            # 清理标题，移除不能用作文件名的字符
            safe_title = self._clean_filename(title)
            
            # 查找所有帖子内容
            posts = soup.find_all('div', class_='bbWrapper')
            
            # 获取主帖内容（第一个帖子）
            if len(posts) >= 1:
                first_post = posts[0]  # 第一个是主帖
                print(f"  找到主帖内容，正在保存...")
                self._save_reply_to_file(first_post, safe_title, save_dir, thread_url)
            else:
                print("  未找到任何内容")
                
        except Exception as e:
            print(f"处理帖子 {thread_url} 时出错: {e}")
            
    def _clean_filename(self, filename: str) -> str:
        """清理文件名，移除不能用作文件名的字符"""
        # 移除或替换不能用作文件名的字符
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # 限制文件名长度
        if len(filename) > 100:
            filename = filename[:100]
            
        return filename.strip()
        
    def _save_reply_to_file(self, post_content, title: str, save_dir: str, thread_url: str):
        """将帖子内容保存为txt文件"""
        try:
            # 获取帖子的纯文本内容，保持分行格式
            text_content = post_content.get_text(separator='\n', strip=True)
            
            # 清理文本格式，保持分行结构
            import re
            # 清理多余的空行，但保持单行换行
            text_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', text_content)
            # 只合并同一行内的多个空格，不影响换行符
            lines = text_content.split('\n')
            cleaned_lines = []
            for line in lines:
                # 清理每行内的多余空格和制表符，但保持行结构
                cleaned_line = re.sub(r'\s+', ' ', line.strip())
                cleaned_lines.append(cleaned_line)
            text_content = '\n'.join(cleaned_lines)
            
            # 构建文件路径
            filename = f"{title}.txt"
            filepath = os.path.join(save_dir, filename)
            
            # 保存内容到文件（只保存纯文本内容）
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text_content)
                
            print(f"  已保存到: {filepath}")
            print(f"  文件大小: {len(text_content)} 字符")
            
        except Exception as e:
            print(f"保存文件时出错: {e}")
            
    def _scrape_thread(self, thread_url: str):
        """爬取单个帖子的翻译内容（保留原方法用于兼容性）"""
        try:
            response = self.session.get(thread_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 获取帖子标题
            title_elem = soup.find('h1', class_='p-title-value')
            title = title_elem.get_text(strip=True) if title_elem else "未知标题"
            print(f"帖子标题: {title}")
            
            # 查找所有帖子内容
            posts = soup.find_all('div', class_='bbWrapper')
            
            # 只处理第一个回复
            if posts:
                print(f"  处理第一个回复...")
                self._extract_translations_from_post(posts[0], title)
            else:
                print("  未找到任何回复内容")
                
        except Exception as e:
            print(f"处理帖子 {thread_url} 时出错: {e}")
            
    def _extract_translations_from_post(self, post_content, thread_title: str):
        """从帖子内容中提取翻译对照"""
        try:
            # 获取纯文本内容
            text_content = post_content.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text_content.split('\n') if line.strip()]
            
            # 方法1: 查找[SET]至[SET COMMENTS]格式的翻译对照
            self._extract_set_pairs(lines, thread_title)
            
            # 方法2: 查找明显的英文-中文对照模式
            self._extract_direct_pairs(lines, thread_title)
            
            # 方法3: 查找引用块中的对照
            self._extract_quote_pairs(post_content, thread_title)
            
            # 方法4: 查找代码块或特殊格式的对照
            self._extract_formatted_pairs(post_content, thread_title)
            
        except Exception as e:
            print(f"    提取翻译时出错: {e}")
            
    def _extract_set_pairs(self, lines: List[str], source: str):
        """提取[SET]至[SET COMMENTS]格式的翻译对照
        
        从同一个帖子中提取所有SET块，然后根据英文内容的相同性进行配对
        """
        # 首先提取所有的SET块
        all_sets = self._extract_all_set_blocks(lines)
        
        if len(all_sets) < 2:
            return
            
        # 分离英文和中文SET块
        english_sets = []
        chinese_sets = []
        
        for set_block in all_sets:
            if self._is_english_set_block(set_block):
                english_sets.append(set_block)
            elif self._is_chinese_set_block(set_block):
                chinese_sets.append(set_block)
                
        print(f"    找到 {len(english_sets)} 个英文SET块, {len(chinese_sets)} 个中文SET块")
        
        # 根据英文内容相同性进行配对
        self._pair_sets_by_english_content(english_sets, chinese_sets, source)
        
    def _extract_all_set_blocks(self, lines: List[str]) -> List[Dict]:
        """提取所有的SET块"""
        set_blocks = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 查找[SET]标记的开始
            if '[SET]' in line.upper() or 'SET]' in line.upper():
                set_content = []
                comments_content = []
                j = i + 1
                
                # 收集SET内容（从[SET]到[SET COMMENTS]）
                while j < len(lines):
                    current_line = lines[j]
                    if '[SET COMMENTS]' in current_line.upper() or 'SET COMMENTS]' in current_line.upper():
                        # 开始收集COMMENTS内容
                        k = j + 1
                        while k < len(lines):
                            comment_line = lines[k]
                            # 如果遇到下一个[SET]或其他结束标记，停止
                            if ('[SET]' in comment_line.upper() or 
                                comment_line.strip() == '' or
                                k == len(lines) - 1):
                                break
                            if comment_line.strip():
                                comments_content.append(comment_line.strip())
                            k += 1
                        break
                    if current_line.strip() and not current_line.startswith('['):
                        set_content.append(current_line.strip())
                    j += 1
                
                if set_content:  # 只有当SET内容不为空时才添加
                    set_blocks.append({
                        'set_content': set_content,
                        'comments_content': comments_content,
                        'start_line': i,
                        'end_line': j
                    })
                    
                i = j if j > i else i + 1
            else:
                i += 1
                
        return set_blocks
        
    def _is_english_set_block(self, set_block: Dict) -> bool:
        """判断SET块是否为英文"""
        set_content = ' '.join(set_block['set_content'])
        return self._is_english_text(set_content)
        
    def _is_chinese_set_block(self, set_block: Dict) -> bool:
        """判断SET块是否为中文"""
        set_content = ' '.join(set_block['set_content'])
        return self._is_chinese_text(set_content)
        
    def _pair_sets_by_english_content(self, english_sets: List[Dict], chinese_sets: List[Dict], source: str):
        """根据英文内容的相同性配对SET块"""
        used_chinese_sets = set()
        
        for en_set in english_sets:
            # 提取英文SET中的关键信息（宝可梦名称、技能等）
            en_key_info = self._extract_set_key_info(en_set['set_content'])
            
            best_match = None
            best_score = 0
            
            for i, cn_set in enumerate(chinese_sets):
                if i in used_chinese_sets:
                    continue
                    
                # 计算匹配度
                match_score = self._calculate_set_match_score(en_key_info, cn_set['set_content'])
                
                if match_score > best_score and match_score > 0.5:  # 设置匹配阈值
                    best_score = match_score
                    best_match = (i, cn_set)
                    
            if best_match:
                used_chinese_sets.add(best_match[0])
                cn_set = best_match[1]
                
                # 创建翻译对
                en_full_content = '\n'.join(en_set['set_content'] + en_set['comments_content'])
                cn_full_content = '\n'.join(cn_set['set_content'] + cn_set['comments_content'])
                
                self.translation_pairs.append({
                    'english': self._clean_text(en_full_content),
                    'chinese': self._clean_text(cn_full_content),
                    'source': source,
                    'type': 'set_matched_pair',
                    'match_score': best_score
                })
                
                print(f"    配对成功 (匹配度: {best_score:.2f}): {en_key_info.get('pokemon', 'Unknown')}")
                
    def _extract_set_key_info(self, set_content: List[str]) -> Dict:
        """从SET内容中提取关键信息"""
        key_info = {
            'pokemon': '',
            'ability': '',
            'item': '',
            'moves': [],
            'nature': '',
            'evs': ''
        }
        
        for line in set_content:
            line_lower = line.lower()
            if 'pokemon:' in line_lower or 'pokémon:' in line_lower:
                key_info['pokemon'] = line.split(':', 1)[1].strip()
            elif 'ability:' in line_lower:
                key_info['ability'] = line.split(':', 1)[1].strip()
            elif 'item:' in line_lower:
                key_info['item'] = line.split(':', 1)[1].strip()
            elif 'nature:' in line_lower:
                key_info['nature'] = line.split(':', 1)[1].strip()
            elif 'evs:' in line_lower:
                key_info['evs'] = line.split(':', 1)[1].strip()
            elif line.strip().startswith('-'):
                move = line.strip()[1:].strip()
                if move:
                    key_info['moves'].append(move)
                    
        return key_info
        
    def _calculate_set_match_score(self, en_key_info: Dict, cn_set_content: List[str]) -> float:
        """计算SET块的匹配分数"""
        score = 0.0
        total_weight = 0.0
        
        cn_content_text = ' '.join(cn_set_content).lower()
        
        # 检查宝可梦名称匹配（权重最高）
        if en_key_info['pokemon']:
            pokemon_en = en_key_info['pokemon'].lower()
            # 简单的宝可梦名称映射（可以扩展）
            pokemon_mapping = {
                'garchomp': '烈咬陆鲨',
                'dragapult': '多龙巴鲁托',
                'landorus': '土地云',
                'rotom': '洛托姆',
                'tyranitar': '班基拉斯'
            }
            
            if pokemon_en in pokemon_mapping:
                if pokemon_mapping[pokemon_en] in cn_content_text:
                    score += 0.4
            total_weight += 0.4
            
        # 检查技能数量匹配
        en_moves_count = len(en_key_info['moves'])
        cn_moves_count = len([line for line in cn_set_content if line.strip().startswith('-')])
        
        if en_moves_count > 0 and cn_moves_count > 0:
            moves_similarity = min(en_moves_count, cn_moves_count) / max(en_moves_count, cn_moves_count)
            score += moves_similarity * 0.3
        total_weight += 0.3
        
        # 检查数字匹配（努力值等）
        en_numbers = set(re.findall(r'\d+', ' '.join([en_key_info['evs']])))
        cn_numbers = set(re.findall(r'\d+', cn_content_text))
        
        if en_numbers and cn_numbers:
            number_overlap = len(en_numbers & cn_numbers) / len(en_numbers | cn_numbers)
            score += number_overlap * 0.3
        total_weight += 0.3
        
        return score / total_weight if total_weight > 0 else 0.0
                
    def _pair_set_contents(self, english_lines: List[str], chinese_lines: List[str], source: str):
        """将英文和中文SET内容进行配对"""
        # 方法1: 按行数配对（如果行数相同）
        if len(english_lines) == len(chinese_lines):
            for en_line, cn_line in zip(english_lines, chinese_lines):
                if self._is_english_text(en_line) and self._is_chinese_text(cn_line):
                    english_clean = self._clean_text(en_line)
                    chinese_clean = self._clean_text(cn_line)
                    
                    if english_clean and chinese_clean:
                        self.translation_pairs.append({
                            'english': english_clean,
                            'chinese': chinese_clean,
                            'source': source,
                            'type': 'set_pair'
                        })
        else:
            # 方法2: 智能配对（基于内容相似性）
            self._smart_pair_contents(english_lines, chinese_lines, source)
            
    def _smart_pair_contents(self, english_lines: List[str], chinese_lines: List[str], source: str):
        """智能配对英文和中文内容"""
        # 简单的启发式配对：寻找相似的结构模式
        used_chinese = set()
        
        for en_line in english_lines:
            if not self._is_english_text(en_line):
                continue
                
            best_match = None
            best_score = 0
            
            for i, cn_line in enumerate(chinese_lines):
                if i in used_chinese or not self._is_chinese_text(cn_line):
                    continue
                    
                # 计算相似度分数（基于长度和结构）
                score = self._calculate_similarity_score(en_line, cn_line)
                
                if score > best_score and score > 0.3:  # 设置最低相似度阈值
                    best_score = score
                    best_match = (i, cn_line)
            
            if best_match:
                used_chinese.add(best_match[0])
                english_clean = self._clean_text(en_line)
                chinese_clean = self._clean_text(best_match[1])
                
                if english_clean and chinese_clean:
                    self.translation_pairs.append({
                        'english': english_clean,
                        'chinese': chinese_clean,
                        'source': source,
                        'type': 'set_smart_pair'
                    })
                    
    def _calculate_similarity_score(self, english_text: str, chinese_text: str) -> float:
        """计算英文和中文文本的相似度分数"""
        # 基于长度比例的相似度
        en_len = len(english_text)
        cn_len = len(chinese_text)
        
        if en_len == 0 or cn_len == 0:
            return 0
            
        # 长度相似度（期望中文比英文短一些）
        length_ratio = min(en_len, cn_len) / max(en_len, cn_len)
        
        # 结构相似度（基于标点符号和数字）
        en_punct = len(re.findall(r'[.,;:!?()\[\]{}"\'-]', english_text))
        cn_punct = len(re.findall(r'[，。；：！？（）\[\]{}"\'-]', chinese_text))
        
        punct_similarity = 1.0
        if en_punct > 0 or cn_punct > 0:
            punct_similarity = min(en_punct, cn_punct) / max(en_punct, cn_punct, 1)
            
        # 数字相似度
        en_numbers = re.findall(r'\d+', english_text)
        cn_numbers = re.findall(r'\d+', chinese_text)
        
        number_similarity = 1.0
        if en_numbers or cn_numbers:
            common_numbers = set(en_numbers) & set(cn_numbers)
            total_numbers = set(en_numbers) | set(cn_numbers)
            number_similarity = len(common_numbers) / len(total_numbers) if total_numbers else 1.0
            
        # 综合相似度分数
        return (length_ratio * 0.4 + punct_similarity * 0.3 + number_similarity * 0.3)
    
    def _extract_direct_pairs(self, lines: List[str], source: str):
        """提取直接的英文-中文对照"""
        i = 0
        while i < len(lines) - 1:
            current_line = lines[i]
            next_line = lines[i + 1]
            
            # 检查是否为英文-中文对照
            if (self._is_english_text(current_line) and 
                self._is_chinese_text(next_line) and
                len(current_line) > 15 and len(next_line) > 5):
                
                # 清理文本
                english_clean = self._clean_text(current_line)
                chinese_clean = self._clean_text(next_line)
                
                if english_clean and chinese_clean:
                    self.translation_pairs.append({
                        'english': english_clean,
                        'chinese': chinese_clean,
                        'source': source,
                        'type': 'direct_pair'
                    })
                    print(f"    找到对照: {english_clean[:50]}... -> {chinese_clean[:30]}...")
                    
            i += 1
            
    def _extract_quote_pairs(self, post_content, source: str):
        """从引用块中提取对照"""
        quotes = post_content.find_all('blockquote')
        for quote in quotes:
            quote_text = quote.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in quote_text.split('\n') if line.strip()]
            self._extract_direct_pairs(lines, source)
            
    def _extract_formatted_pairs(self, post_content, source: str):
        """从格式化内容中提取对照"""
        # 查找代码块
        code_blocks = post_content.find_all(['code', 'pre'])
        for block in code_blocks:
            block_text = block.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in block_text.split('\n') if line.strip()]
            self._extract_direct_pairs(lines, source)
            
        # 查找表格
        tables = post_content.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    english_cell = cells[0].get_text(strip=True)
                    chinese_cell = cells[1].get_text(strip=True)
                    
                    if (self._is_english_text(english_cell) and 
                        self._is_chinese_text(chinese_cell)):
                        
                        english_clean = self._clean_text(english_cell)
                        chinese_clean = self._clean_text(chinese_cell)
                        
                        if english_clean and chinese_clean:
                            self.translation_pairs.append({
                                'english': english_clean,
                                'chinese': chinese_clean,
                                'source': source,
                                'type': 'table_pair'
                            })
                            
    def _is_english_text(self, text: str) -> bool:
        """判断文本是否主要为英文"""
        if not text or len(text) < 5:
            return False
            
        # 移除标点和数字
        alpha_chars = re.sub(r'[^a-zA-Z]', '', text)
        if len(alpha_chars) < 3:
            return False
            
        # 检查英文字符比例
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        total_chars = len(text.replace(' ', ''))
        
        if total_chars == 0:
            return False
            
        english_ratio = english_chars / total_chars
        return english_ratio > 0.6
        
    def _is_chinese_text(self, text: str) -> bool:
        """判断文本是否主要为中文"""
        if not text or len(text) < 2:
            return False
            
        # 计算中文字符比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        total_chars = len(text.replace(' ', ''))
        
        if total_chars == 0:
            return False
            
        chinese_ratio = chinese_chars / total_chars
        return chinese_ratio > 0.3
        
    def _clean_text(self, text: str) -> str:
        """清理文本内容"""
        if not text:
            return ""
            
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text.strip())
        
        # 移除特殊标记
        text = re.sub(r'^[\d\s\-\*\+\.]+', '', text)  # 移除开头的数字、符号
        text = re.sub(r'[\r\n\t]', ' ', text)  # 移除换行符
        
        # 移除引用标记
        text = re.sub(r'^(>|>>|>>>)\s*', '', text)
        
        return text.strip()
        
    def save_translations(self, filename: str = "smogon_translations.json", format_type: str = "json"):
        """保存翻译对照到文件
        
        Args:
            filename: 保存的文件名
            format_type: 保存格式 ('json', 'csv', 'txt', 'xlsx')
        """
        try:
            # 确保保存目录存在
            save_dir = os.path.dirname(filename) if os.path.dirname(filename) else "./scraped_data"
            if not os.path.exists(save_dir) and save_dir != "./scraped_data":
                os.makedirs(save_dir, exist_ok=True)
            elif save_dir == "./scraped_data":
                os.makedirs("scraped_data", exist_ok=True)
                filename = os.path.join("scraped_data", os.path.basename(filename))
            
            if format_type.lower() == "json":
                self._save_as_json(filename)
            elif format_type.lower() == "csv":
                self._save_as_csv(filename)
            elif format_type.lower() == "txt":
                self._save_as_txt(filename)
            elif format_type.lower() == "xlsx":
                self._save_as_xlsx(filename)
            else:
                print(f"不支持的格式: {format_type}，使用JSON格式保存")
                self._save_as_json(filename)
                
        except Exception as e:
            print(f"保存文件时出错: {e}")
            
    def _save_as_json(self, filename: str):
        """保存为JSON格式"""
        if not filename.endswith('.json'):
            filename += '.json'
            
        data = {
            'metadata': {
                'total_count': len(self.translation_pairs),
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'processed_urls': list(self.processed_urls),
                'scraper_version': '1.0'
            },
            'translation_pairs': self.translation_pairs,
            'statistics': self._get_statistics()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"\n翻译对照已保存到: {filename} (JSON格式)")
        print(f"共保存 {len(self.translation_pairs)} 个翻译对照")
        
    def _save_as_csv(self, filename: str):
        """保存为CSV格式"""
        import csv
        
        if not filename.endswith('.csv'):
            filename += '.csv'
            
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['英文原文', '中文翻译', '来源', '类型', '长度(英文)', '长度(中文)'])
            
            for pair in self.translation_pairs:
                writer.writerow([
                    pair['english'],
                    pair['chinese'],
                    pair.get('source', ''),
                    pair.get('type', ''),
                    len(pair['english']),
                    len(pair['chinese'])
                ])
                
        print(f"\n翻译对照已保存到: {filename} (CSV格式)")
        print(f"共保存 {len(self.translation_pairs)} 个翻译对照")
        
    def _save_as_txt(self, filename: str):
        """保存为TXT格式"""
        if not filename.endswith('.txt'):
            filename += '.txt'
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Smogon论坛翻译对照数据\n")
            f.write(f"爬取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总数量: {len(self.translation_pairs)}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, pair in enumerate(self.translation_pairs, 1):
                f.write(f"对照 {i}:\n")
                f.write(f"英文: {pair['english']}\n")
                f.write(f"中文: {pair['chinese']}\n")
                f.write(f"来源: {pair.get('source', '未知')}\n")
                f.write(f"类型: {pair.get('type', '未知')}\n")
                f.write("-" * 30 + "\n\n")
                
        print(f"\n翻译对照已保存到: {filename} (TXT格式)")
        print(f"共保存 {len(self.translation_pairs)} 个翻译对照")
        
    def _save_as_xlsx(self, filename: str):
        """保存为Excel格式"""
        try:
            import pandas as pd
            
            if not filename.endswith('.xlsx'):
                filename += '.xlsx'
                
            # 准备数据
            data = []
            for pair in self.translation_pairs:
                data.append({
                    '英文原文': pair['english'],
                    '中文翻译': pair['chinese'],
                    '来源': pair.get('source', ''),
                    '类型': pair.get('type', ''),
                    '英文长度': len(pair['english']),
                    '中文长度': len(pair['chinese']),
                    '英文词数': len(pair['english'].split()),
                    '中文字数': len(pair['chinese'].replace(' ', ''))
                })
                
            df = pd.DataFrame(data)
            
            # 创建Excel文件
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='翻译对照', index=False)
                
                # 添加统计信息
                stats_data = {
                    '统计项目': ['总数量', '平均英文长度', '平均中文长度', '爬取时间'],
                    '数值': [
                        len(self.translation_pairs),
                        f"{sum(len(p['english']) for p in self.translation_pairs) / len(self.translation_pairs):.1f}" if self.translation_pairs else "0",
                        f"{sum(len(p['chinese']) for p in self.translation_pairs) / len(self.translation_pairs):.1f}" if self.translation_pairs else "0",
                        time.strftime('%Y-%m-%d %H:%M:%S')
                    ]
                }
                stats_df = pd.DataFrame(stats_data)
                stats_df.to_excel(writer, sheet_name='统计信息', index=False)
                
            print(f"\n翻译对照已保存到: {filename} (Excel格式)")
            print(f"共保存 {len(self.translation_pairs)} 个翻译对照")
            
        except ImportError:
            print("需要安装pandas和openpyxl库才能保存Excel格式")
            print("请运行: pip install pandas openpyxl")
            print("改为保存JSON格式...")
            self._save_as_json(filename.replace('.xlsx', '.json'))
            
    def _get_statistics(self) -> dict:
        """获取爬取数据的统计信息"""
        if not self.translation_pairs:
            return {}
            
        # 按来源统计
        source_count = {}
        type_count = {}
        
        english_lengths = []
        chinese_lengths = []
        
        for pair in self.translation_pairs:
            source = pair.get('source', '未知来源')
            pair_type = pair.get('type', '未知类型')
            
            source_count[source] = source_count.get(source, 0) + 1
            type_count[pair_type] = type_count.get(pair_type, 0) + 1
            
            english_lengths.append(len(pair['english']))
            chinese_lengths.append(len(pair['chinese']))
            
        return {
            'source_distribution': source_count,
            'type_distribution': type_count,
            'length_statistics': {
                'avg_english_length': sum(english_lengths) / len(english_lengths),
                'avg_chinese_length': sum(chinese_lengths) / len(chinese_lengths),
                'max_english_length': max(english_lengths),
                'max_chinese_length': max(chinese_lengths),
                'min_english_length': min(english_lengths),
                'min_chinese_length': min(chinese_lengths)
            }
        }
            
    def load_into_translator(self, translator_instance):
        """将爬取的翻译对照加载到翻译器中"""
        added_count = 0
        for pair in self.translation_pairs:
            try:
                translator_instance.add_translation_sample(
                    pair['english'], 
                    pair['chinese']
                )
                added_count += 1
            except Exception as e:
                print(f"添加翻译样本时出错: {e}")
                
        print(f"成功添加 {added_count} 个翻译样本到翻译器")
        
    def print_summary(self):
        """打印爬取结果摘要"""
        print("\n=== 爬取结果摘要 ===")
        print(f"总翻译对照数: {len(self.translation_pairs)}")
        
        # 按来源统计
        source_count = {}
        type_count = {}
        
        for pair in self.translation_pairs:
            source = pair.get('source', '未知来源')
            pair_type = pair.get('type', '未知类型')
            
            source_count[source] = source_count.get(source, 0) + 1
            type_count[pair_type] = type_count.get(pair_type, 0) + 1
            
        print("\n按来源统计:")
        for source, count in sorted(source_count.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {source[:50]}...: {count} 个")
            
        print("\n按类型统计:")
        for pair_type, count in type_count.items():
            print(f"  {pair_type}: {count} 个")
            
        # 显示一些示例
        print("\n翻译对照示例:")
        for i, pair in enumerate(self.translation_pairs[:3]):
            print(f"\n示例 {i+1}:")
            print(f"  英文: {pair['english']}")
            print(f"  中文: {pair['chinese']}")
            print(f"  来源: {pair.get('source', '未知')}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Smogon论坛翻译内容爬虫')
    parser.add_argument('--url', type=str, 
                       default="https://www.smogon.com/forums/forums/chinese-sv-analysis-archive.824/?prefix_id=484",
                       help='要爬取的Smogon论坛URL')
    parser.add_argument('--format', type=str, choices=['json', 'csv', 'txt', 'xlsx'], 
                       default='json', help='保存格式')
    parser.add_argument('--output', type=str, default='smogon_translations', 
                       help='输出文件名（不含扩展名）')
    parser.add_argument('--max-threads', type=int, default=10, 
                       help='最大处理帖子数量')
    parser.add_argument('--load-to-translator', action='store_true', 
                       help='自动加载到翻译器')
    parser.add_argument('--save-all-formats', action='store_true', 
                       help='保存所有格式')
    
    args = parser.parse_args()
    
    scraper = SmogonScraper()
    
    print(f"开始爬取: {args.url}")
    print(f"最大处理帖子数: {args.max_threads}")
    
    # 爬取中文翻译存档，保存为txt文件
    scraper.scrape_chinese_archive(args.url)
    
    print("\n爬取完成！")
    
    # 显示保存的文件
    save_dir = "scraped_threads"
    if os.path.exists(save_dir):
        files = os.listdir(save_dir)
        if files:
            print(f"\n保存的文件 (共{len(files)}个):")
            for file in sorted(files)[:10]:  # 只显示前10个文件
                file_path = os.path.join(save_dir, file)
                file_size = os.path.getsize(file_path)
                print(f"  {file} ({file_size} 字节)")
            if len(files) > 10:
                print(f"  ... 还有 {len(files) - 10} 个文件")
        else:
            print("\n没有保存任何文件")
    else:
        print("\n保存目录不存在")
        
if __name__ == "__main__":
    main()