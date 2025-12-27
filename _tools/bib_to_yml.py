import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import yaml
import os
import re

# NASA ADS Journal Macros 對照表
# 您可以根據 https://ui.adsabs.harvard.edu/help/actions/journal-macros 繼續增加
ADS_JOURNAL_MACROS = {
    r'\aj': 'Astron. J.',
    r'\actaa': 'Acta Astron.',
    r'\araa': 'Annu. Rev. Astron. Astrophys.',
    r'\apj': 'Astrophys. J.',
    r'\apjl': 'Astrophys. J. Lett.',
    r'\apjs': 'Astrophys. J. Suppl. Ser.',
    r'\ao': 'Appl. Opt.',
    r'\apss': 'Astrophys. Space Sci.',
    r'\aap': 'Astron. Astrophys.',
    'åp': 'Astron. Astrophys.',    # 處理 \aap -> å + p
    r'\aapr': 'Astron. Astrophys. Rev.',
    'åpr': 'Astron. Astrophys. Rev.', # 處理 \aapr -> å + pr
    r'\aaps': 'Astron. Astrophys. Suppl.',
    'åps': 'Astron. Astrophys. Suppl.', # 處理 \aaps -> å + ps
    r'\azh': 'Astron. Zh.',
    r'\baas': 'Bull. Am. Astron. Soc.',
    r'\caa': 'Chin. Astron. Astrophys.',
    r'\cjaa': 'Chin. J. Astron. Astrophys.',
    r'\icarus': 'Icarus',
    r'\jcap': 'J. Cosmol. Astropart. Phys.',
    r'\jrasc': 'J. R. Astron. Soc. Can.',
    r'\memras': 'Mem. R. Astron. Soc.',
    r'\memsai': 'Mem. Soc. Astron. Ital.',
    r'\mnras': 'Mon. Not. R. Astron. Soc.',
    r'\na': 'New Astron.',
    r'\nar': 'New Astron. Rev.',
    r'\nat': 'Nature',
    r'\nphys': 'Nat. Phys.',
    r'\pasa': 'Publ. Astron. Soc. Aust.',
    r'\pasp': 'Publ. Astron. Soc. Pac.',
    r'\pasj': 'Publ. Astron. Soc. Jpn.',
    r'\physrep': 'Phys. Rep.',
    r'\physscr': 'Phys. Scr.',
    r'\pra': 'Phys. Rev. A',
    r'\prb': 'Phys. Rev. B',
    r'\prc': 'Phys. Rev. C',
    r'\prd': 'Phys. Rev. D',
    r'\pre': 'Phys. Rev. E',
    r'\prl': 'Phys. Rev. Lett.',
    r'\rmxaa': 'Rev. Mex. Astron. Astrofis.',
    r'\qjras': 'Q. J. R. Astron. Soc.',
    r'\sci': 'Science',
    r'\skytel': 'Sky Telesc.',
    r'\solphys': 'Sol. Phys.',
    r'\sovast': 'Sov. Astron.',
    r'\ssr': 'Space Sci. Rev.',
    r'\zap': 'Z. Astrophys.',
}

# 配置
BIB_FILE = 'export-bibtex.bib'
MEMBERS_FILE = '../_data/members.yml'
OUTPUT_YAML_FILE = '../_data/publications.yml'

def load_members():
    """載入成員及其別名"""
    member_data = []
    if os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            for m in data:
                # 收集主名字和所有別名
                names = [m['name']]
                if 'aliases' in m and m['aliases']:
                    names.extend(m['aliases'])
                member_data.append({"main_name": m['name'], "search_names": names})
    return member_data

def get_existing_tags():
    """保留原本 YAML 裡的標籤"""
    tag_map = {}
    if os.path.exists(OUTPUT_YAML_FILE):
        with open(OUTPUT_YAML_FILE, 'r', encoding='utf-8') as f:
            old_data = yaml.safe_load(f)
            if old_data:
                for pub in old_data:
                    # 使用標題作為唯一識別（轉小寫去掉空格）
                    clean_title = re.sub(r'\W+', '', pub['title'].lower())
                    tag_map[clean_title] = pub.get('tags', [])
    return tag_map

def normalize_name(name):
    """將名字正規化：移除所有非字母字元並轉小寫"""
    if not name: return ""
    # 移除標點符號、括號、反斜槓、空格、連字號
    return re.sub(r'[^a-zA-Z]', '', name).lower()

def process_author_name(author_str, member_db):
    """處理 BibTeX 作者字串，比對成員名單並加粗"""
    # BibTeX 作者通常以 ' and ' 分隔
    authors = author_str.replace('\n', ' ').split(' and ')
    final_authors = []

    for a in authors:
        # 1. 基礎清理
        a = a.strip().replace('{', '').replace('}', '')
        
        # 處理 BibTeX 的 "Last, First" 格式
        current_display_name = a
        if ',' in a:
            parts = a.split(',')
            current_display_name = f"{parts[1].strip()} {parts[0].strip()}"
        
        # 2. 生成目前作者的正規化 ID (例如: hsiyuschive)
        norm_a = normalize_name(current_display_name)

        matched_main_name = None
        
        # 3. 比對成員資料庫
        for m in member_db:
            # 檢查主名字與所有別名
            for alias in m['search_names']:
                if normalize_name(alias) == norm_a:
                    matched_main_name = m['main_name']
                    break
            if matched_main_name: break

        # 4. 如果匹配成功，顯示主名字並加粗
        if matched_main_name:
            final_authors.append(f"<strong>{current_display_name}</strong>")
        else:
            final_authors.append(current_display_name)

    # 5. 結合所有作者
    if len(final_authors) > 1:
        return ", ".join(final_authors[:-1]) + ", and " + final_authors[-1]
    return final_authors[0] if final_authors else ""

def process_journal_name(raw_journal):
    if not raw_journal:
        return ""
    
    # 移除多餘的括號與反斜槓，保留核心巨集名稱 (如 \apj)
    clean_j = raw_journal.strip().replace('{', '').replace('}', '')
    
    # 檢查是否在對照表中 (完全比對或部分取代)
    for macro, full_name in ADS_JOURNAL_MACROS.items():
        if macro == clean_j:
            clean_j = clean_j.replace(macro, full_name)
    # 最後再把剩下的反斜槓去掉（萬一有不在表中的巨集）
    return clean_j.replace('\\', '')

# --- 在 convert() 迴圈內使用 ---
# journal = process_journal_name(entry.get('journal', ''))

def convert():
    member_db = load_members()
    tag_map = get_existing_tags()
    
    with open(BIB_FILE, 'r', encoding='utf-8') as bibfile:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibfile, parser=parser)

    output_pubs = []
    for entry in bib_database.entries:
        if entry.get('ENTRYTYPE').lower() != 'article':
            continue
        title = entry.get('title', '').replace('{', '').replace('}', '')
        clean_title_key = re.sub(r'\W+', '', title.lower())
        
        pub = {
            'year': entry.get('year', ''),
            'month': entry.get('month', ''),
            'title': title,
            'authors': process_author_name(entry.get('author', ''), member_db),
            'journal': process_journal_name(entry.get('journal', '')),
            'volume': entry.get('volume', ''),
            'number': entry.get('number', ''),
            'pages': entry.get('pages', ''),
            'link_value': f"https://doi.org/{entry.get('doi', '')}" if 'doi' in entry else entry.get('adsurl', ''),
            'tags': tag_map.get(clean_title_key, []) # 抓回舊標籤
        }
        output_pubs.append(pub)

    # 排序：年份降序
    output_pubs.sort(key=lambda x: x['year'], reverse=True)

    with open(OUTPUT_YAML_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(output_pubs, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    convert()