# -*- coding: utf-8 -*-
"""
URL翻译器演示版本
直接处理指定URL并展示翻译结果
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from typing import Dict, List, Any

def scrape_and_translate_url(url: str):
    """爬取并翻译指定URL的内容"""
    
    # 初始化HTTP会话
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    # 术语词典
    term_dictionary = {
        'Garchomp': '烈咬陆鲨',
        'Giratina-O': '骑拉帝纳-起源',
        'Giratina': '骑拉帝纳',
        'Landorus-T': '土地云-灵兽',
        'Clefable': '皮可西',
        'Heatran': '席多蓝恩',
        'Scizor': '巨钳螳螂',
        'Kartana': '纸御剑',
        'Zapdos': '闪电鸟',
        'Ho-Oh': '凤王',
        'Arceus': '阿尔宙斯',
        'Kyogre': '盖欧卡',
        'Koraidon': '故勒顿',
        'Miraidon': '密勒顿',
        'Necrozma-DM': '奈克洛兹玛-黄昏之鬃',
        'Ting-Lu': '古鼎鹿',
        'Gliscor': '天蝎王',
        'Chien-Pao': '古剑豹',
        'Clodsire': '土王',
        'Shadow Ball': '影子球',
        'Dragon Dance': '龙之舞',
        'Calm Mind': '冥想',
        'Will-O-Wisp': '磷火',
        'Stone Edge': '尖石攻击',
        'Thunder Wave': '电磁波',
        'Scale Shot': '鳞射',
        'Stealth Rock': '隐形岩',
        'Hex': '祸不单行',
        'Poltergeist': '灵骚',
        'Dragon Tail': '龙尾',
        'Defog': '清雾',
        'Shadow Sneak': '影子偷袭',
        'Shadow Claw': '影爪',
        'Draco Meteor': '流星群',
        'Extreme Speed': '神速',
        'Knock Off': '拍落',
        'Taunt': '挑衅',
        'Ruination': '大灾难',
        'Flare Blitz': '闪焰冲锋',
        'Toxic': '剧毒',
        'Levitate': '飘浮',
        'Griseous Core': '白金宝珠',
        'Life Orb': '生命宝珠',
        'Choice Band': '讲究头带',
        'Choice Specs': '讲究眼镜',
        'Leftovers': '吃剩的东西',
        'setup sweeper': '强化清场手',
        'physical bulk': '物理耐久',
        'special bulk': '特殊耐久',
        'entry hazards': '入场危险',
        'priority moves': '先制招式',
        'super effective': '效果拔群',
        'not very effective': '效果不佳',
        'immune to': '免疫',
        'STAB': '本系加成',
        'Ghost-types': '幽灵系',
        'Dragon-types': '龙系',
        'Steel-types': '钢系',
        'Poison-types': '毒系',
        'Fairy-types': '妖精系',
        'Ground-types': '地面系',
        'Fire-types': '火系',
        'Electric-types': '电系',
        'Terastallization': '太晶化',
        'Tera Steel': '太晶钢',
        'Tera Ghost': '太晶幽灵',
        'Tera Poison': '太晶毒',
        'wallbreakers': '破墙手',
        'defensive cores': '防御核心',
        'chip damage': '削弱伤害'
    }
    
    # 一般词汇
    general_vocab = {
        'strong': '强力的',
        'powerful': '强大的',
        'effective': '有效的',
        'reliable': '可靠的',
        'consistent': '稳定的',
        'versatile': '多样的',
        'bulky': '耐久的',
        'frail': '脆弱的',
        'offensive': '进攻性的',
        'defensive': '防御性的',
        'notable': '值得注意的',
        'distinct': '独特的',
        'unique': '独特的',
        'high': '高的',
        'low': '低的',
        'great': '很好的',
        'excellent': '优秀的',
        'fantastic': '极好的',
        'immense': '巨大的',
        'critical': '关键的',
        'useful': '有用的',
        'valuable': '有价值的',
        'tanky': '坦克型的',
        'check': '制衡',
        'counter': '克制',
        'threaten': '威胁',
        'pressure': '施压',
        'support': '支援',
        'handle': '应对',
        'cover': '覆盖',
        'boost': '提升',
        'lower': '降低',
        'hits': '命中',
        'lacks': '缺乏',
        'limits': '限制',
        'provides': '提供',
        'enables': '使能够',
        'maintains': '维持',
        'negates': '否定',
        'allows': '允许',
        'combined': '结合',
        'access': '获得',
        'resist': '抵抗',
        'appreciate': '欣赏',
        'recovery': '回复',
        'ability': '能力',
        'threats': '威胁',
        'team': '队伍',
        'strategy': '策略',
        'weakness': '弱点',
        'Attack': '攻击',
        'Defense': '防御',
        'Speed': '速度',
        'HP': '体力',
        'niche': '定位',
        'typing': '属性',
        'standards': '标准',
        'disposal': '支配',
        'utility': '实用性',
        'tier': '分级',
        'combination': '组合',
        'advantage': '优势',
        'management': '管理',
        'options': '选择',
        'mention': '提及',
        'partners': '搭档',
        'damage': '伤害',
        'time': '时间'
    }
    
    try:
        print(f"正在爬取URL: {url}")
        
        # 发送请求
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        # 解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 获取帖子标题
        title_elem = soup.find('h1', class_='p-title-value')
        title = title_elem.get_text(strip=True) if title_elem else "未知标题"
        
        # 查找第一个帖子内容
        first_post = soup.find('div', class_='bbWrapper')
        
        if not first_post:
            print("未找到帖子内容")
            return None
        
        # 提取纯文本内容
        text_content = first_post.get_text(separator='\n', strip=True)
        
        # 清理文本格式
        lines = text_content.split('\n')
        cleaned_lines = []
        for line in lines:
            cleaned_line = re.sub(r'\s+', ' ', line.strip())
            if cleaned_line:  # 只保留非空行
                cleaned_lines.append(cleaned_line)
        
        original_content = '\n'.join(cleaned_lines)
        
        print(f"成功爬取帖子: {title}")
        print(f"内容长度: {len(original_content)} 字符")
        
        # 翻译内容
        print("\n正在翻译内容...")
        translated_content = original_content
        
        # 应用术语翻译（按长度降序排序）
        sorted_terms = sorted(term_dictionary.items(), key=lambda x: len(x[0]), reverse=True)
        for en_term, cn_term in sorted_terms:
            pattern = r'\b' + re.escape(en_term) + r'\b'
            translated_content = re.sub(pattern, cn_term, translated_content, flags=re.IGNORECASE)
        
        # 应用语法结构转换
        grammar_patterns = {
            r'However, (.+)': r'然而，\1',
            r'While (.+), (.+)': r'虽然\1，但是\2',
            r'Although (.+), (.+)': r'尽管\1，\2',
            r'(\w+) can (.+)': r'\1能够\2',
            r'access to (.+)': r'获得\1',
            r'most notable for (.+)': r'最值得注意的是\1',
            r'makes up for (.+) with (.+)': r'用\2弥补\1',
            r'in combination with (.+)': r'与\1结合'
        }
        
        for pattern, replacement in grammar_patterns.items():
            translated_content = re.sub(pattern, replacement, translated_content, flags=re.IGNORECASE)
        
        # 应用一般词汇翻译
        sorted_vocab = sorted(general_vocab.items(), key=lambda x: len(x[0]), reverse=True)
        for en_word, cn_word in sorted_vocab:
            pattern = r'\b' + re.escape(en_word) + r'\b'
            translated_content = re.sub(pattern, cn_word, translated_content, flags=re.IGNORECASE)
        
        # 分析翻译质量
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', translated_content))
        total_chars = len(translated_content.replace(' ', ''))
        chinese_ratio = chinese_chars / total_chars if total_chars > 0 else 0
        
        # 计算术语覆盖率
        found_terms = sum(1 for term in term_dictionary.keys() if term.lower() in original_content.lower())
        translated_terms = sum(1 for cn_term in term_dictionary.values() if cn_term in translated_content)
        term_coverage = translated_terms / found_terms if found_terms > 0 else 0
        
        # 语法得分
        grammar_indicators = ['能够', '然而', '虽然', '尽管', '与', '结合']
        grammar_score = min(1.0, sum(1 for indicator in grammar_indicators if indicator in translated_content) * 0.2)
        
        # 总体质量
        overall_quality = (chinese_ratio * 0.3 + term_coverage * 0.4 + grammar_score * 0.3)
        
        result = {
            'url': url,
            'title': title,
            'original_content': original_content,
            'translated_content': translated_content,
            'translation_quality': {
                'chinese_ratio': chinese_ratio,
                'term_coverage': term_coverage,
                'grammar_score': grammar_score,
                'overall_quality': overall_quality
            },
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"翻译完成，质量评分: {overall_quality:.3f}")
        
        # 保存结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'demo_url_translation_{timestamp}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n结果已保存到: {output_file}")
        
        # 显示结果摘要
        print("\n=== 翻译结果摘要 ===")
        print(f"标题: {title}")
        print(f"\n原文内容 (前300字符):")
        print(original_content[:300] + "..." if len(original_content) > 300 else original_content)
        print(f"\n翻译内容 (前300字符):")
        print(translated_content[:300] + "..." if len(translated_content) > 300 else translated_content)
        print(f"\n翻译质量:")
        print(f"  中文比例: {chinese_ratio:.3f}")
        print(f"  术语覆盖率: {term_coverage:.3f}")
        print(f"  语法得分: {grammar_score:.3f}")
        print(f"  总体质量: {overall_quality:.3f}")
        
        return result
        
    except Exception as e:
        print(f"处理失败: {e}")
        return None

if __name__ == '__main__':
    # 处理用户提供的示例URL
    demo_url = "https://www.smogon.com/forums/threads/physical-giratina-o.3739313/"
    print("=== URL翻译器演示 ===")
    print(f"处理URL: {demo_url}")
    print("\n" + "="*60)
    
    result = scrape_and_translate_url(demo_url)
    
    if result:
        print("\n演示完成！")
    else:
        print("\n演示失败！")