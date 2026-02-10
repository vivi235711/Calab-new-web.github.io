import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import yaml
import os
import re

# Get current script directory path (_tools)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BIB_FILE = os.path.join(BASE_DIR, 'export-bibtex.bib')
MEMBERS_FILE = os.path.join(BASE_DIR, '..', '_data', 'members.yml')
OUTPUT_YAML_FILE = os.path.join(BASE_DIR, '..', '_data', 'publications.yml')

# NASA ADS Journal Macros mapping
# Refer to https://ui.adsabs.harvard.edu/help/actions/journal-macros for additions
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
    'åp': 'Astron. Astrophys.',    # Handle \aap -> å + p
    r'\aapr': 'Astron. Astrophys. Rev.',
    'åpr': 'Astron. Astrophys. Rev.', # Handle \aapr -> å + pr
    r'\aaps': 'Astron. Astrophys. Suppl.',
    'åps': 'Astron. Astrophys. Suppl.', # Handle \aaps -> å + ps
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



def load_members():
    """Load members and their aliases for matching author names"""
    member_data = []
    if os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            for m in data:
                # Collect main name and all aliases
                names = [m['english_name']]
                if 'aliases' in m and m['aliases']:
                    names.extend(m['aliases'])
                member_data.append({"main_name": m['english_name'], "search_names": names})
    return member_data

def get_existing_tags():
    """Retain existing tags from the YAML file"""
    tag_map = {}
    if os.path.exists(OUTPUT_YAML_FILE):
        with open(OUTPUT_YAML_FILE, 'r', encoding='utf-8') as f:
            old_data = yaml.safe_load(f)
            if old_data:
                for pub in old_data:
                    # Use lowercase title with spaces removed as unique identifier
                    clean_title = re.sub(r'\W+', '', pub['title'].lower())
                    tag_map[clean_title] = pub.get('tags', [])
    return tag_map

def normalize_name(name):
    """Normalize name: remove non-alphabetic characters and convert to lowercase"""
    if not name: return ""
    # Remove punctuation, brackets, backslashes, spaces, hyphens
    return re.sub(r'[^a-zA-Z]', '', name).lower()

def process_author_name(author_str, member_db):
    """Process BibTeX author string, cross-reference member list, and bold matches"""
    # BibTeX authors are typically separated by ' and '
    authors = author_str.replace('\n', ' ').split(' and ')
    final_authors = []

    for a in authors:
        # 1. Basic Cleaning
        a = a.strip().replace('{', '').replace('}', '')
        
        # Handle BibTeX "Last, First" format
        current_display_name = a
        if ',' in a:
            parts = a.split(',')
            current_display_name = f"{parts[1].strip()} {parts[0].strip()}"
        
        # 2. Generate normalized ID for current author (e.g., hsiyuschive)
        norm_a = normalize_name(current_display_name)

        matched_main_name = None
        
        # 3. Match against member database
        for m in member_db:
            # Check main name and all aliases
            for alias in m['search_names']:
                if normalize_name(alias) == norm_a:
                    matched_main_name = m['main_name']
                    break
            if matched_main_name: break

        # 4. Bold display name if match is successful
        if matched_main_name:
            final_authors.append(f"<strong>{current_display_name}</strong>")
        else:
            final_authors.append(current_display_name)

    # 5. Join all authors
    if len(final_authors) > 1:
        return ", ".join(final_authors[:-1]) + ", and " + final_authors[-1]
    return final_authors[0] if final_authors else ""

def process_journal_name(raw_journal):
    """Process journal name by removing redundant braces and backslashes, and replacing macros with full names"""
    if not raw_journal:
        return ""
    
    # Remove redundant brackets and backslashes, keeping core macro name (e.g., \apj)
    clean_j = raw_journal.strip().replace('{', '').replace('}', '')
    
    # Check mapping table (exact match or partial replacement)
    for macro, full_name in ADS_JOURNAL_MACROS.items():
        if macro == clean_j:
            clean_j = clean_j.replace(macro, full_name)
    # Remove remaining backslashes (for macros not in the table)
    return clean_j.replace('\\', '')

ENSUREMATH_RE = re.compile(r'{?\\ensuremath\s*(?:{([^{}]+)}|\\?([^\s{}]+))}?')

def clean_title(raw_title: str) -> str:
    """Clean title by removing redundant braces and ensuring math expressions are properly formatted"""
    if not raw_title:
        return ""
    title = raw_title.strip()

    def _ensure(m):
        content = m.group(1) or m.group(2) or ""
        return f"${content.strip()}$"
    title = ENSUREMATH_RE.sub(_ensure, title)

    # Preserve braces elsewhere; only tidy whitespace
    title = re.sub(r'\s+', ' ', title).strip()
    title = title.replace('{', '').replace('}', '')
    return title

# --- Used within convert() loop ---

def convert():
    member_db = load_members()
    tag_map = get_existing_tags()
    
    with open(BIB_FILE, 'r', encoding='utf-8') as bibfile:
        parser = BibTexParser()
        # parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibfile, parser=parser)

    output_pubs = []
    for entry in bib_database.entries:

        author_raw = entry.get('author', '')
        authors = convert_to_unicode({'author': author_raw}).get('author', author_raw)

        title = entry.get('title', '')
        title = clean_title(title)
        clean_title_key = re.sub(r'\W+', '', title.lower())

        pub = {
            'year': entry.get('year', ''),
            'month': entry.get('month', ''),
            'title': title,
            'authors': process_author_name(authors, member_db),
            'journal': process_journal_name(entry.get('journal', '')),
            'volume': entry.get('volume', ''),
            'number': entry.get('number', ''),
            'pages': entry.get('pages', ''),
            'link_value': f"https://doi.org/{entry.get('doi', '')}" if 'doi' in entry else entry.get('adsurl', '') or entry.get('url', '') or entry.get('URL', ''),
            'type': entry.get('ENTRYTYPE', '').lower(),
            'tags': tag_map.get(clean_title_key, []) # Retrieve old tags
        }
        output_pubs.append(pub)

    # Sort: Year Descending
    output_pubs.sort(key=lambda x: x['year'], reverse=True)

    with open(OUTPUT_YAML_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(output_pubs, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    convert()