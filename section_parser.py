import re
from collections import Counter
from section_keyword import SECTION_KEYWORDS

# --- Helper Functions ---

def get_body_font_stats(lines):
    """Returns the most common font size and name to use as a baseline."""
    if not lines:
        return 10.0, "Unknown"
        
    sizes = [l["font_size"] for l in lines]
    font_names = [l["font_name"] for l in lines if l.get("font_name")]
    
    body_size = Counter(sizes).most_common(1)[0][0] if sizes else 10.0
    body_font = Counter(font_names).most_common(1)[0][0] if font_names else None
    
    return body_size, body_font

def match_section_keyword(text):
    """Checks if text matches any of the defined section keywords."""
    t = re.sub(r'[^a-z ]', '', text.lower())
    for section, keywords in SECTION_KEYWORDS.items():
        for k in keywords:
            # Match exact word boundary
            pattern = r'\b' + re.escape(k) + r'\b'
            if re.search(pattern, t):
                return section
    return None

def is_header_line(line, body_size, body_font_name=None):
    """
    Scoring system to determine if a line is a section header.
    """
    score = 0
    text = line["text"]

    # Rule 1: Font Size (Larger than body)
    if line["font_size"] >= body_size * 1.2:
        score += 2

    # Rule 2: Bold or Distinct Font
    if line.get("bold_ratio", 0) > 0.6:
        score += 1
    elif body_font_name and line.get("font_name") != body_font_name:
        score += 1

    # Rule 3: Uppercase
    if text.isupper():
        score += 1

    # Rule 4: Length (Short lines are more likely headers)
    if len(text.split()) <= 4:
        score += 1
    
    # Rule 5: Keywords (Strongest indicator)
    if match_section_keyword(text):
        score += 2

    # Threshold: score >= 5 implies it is a header
    return score >= 5

# --- Main Logic ---

def process_lines_to_sections(lines):
    """
    Takes raw lines, detects headers, and groups content into sections.
    """
    if not lines:
        return {}

    # 1. Analyze the document style
    body_size, body_font_name = get_body_font_stats(lines)
    
    # 2. Tag lines as headers
    misc_count = 0
    labeled_lines = []
    
    for l in lines:
        if is_header_line(l, body_size, body_font_name):
            l["is_header"] = True
            section_type = match_section_keyword(l["text"])
            
            if section_type:
                # Create unique section name combining section type and actual text
                l["section"] = f"{section_type}-{l['text']}"
            else:
                l["section"] = f"misc_{misc_count}"
                misc_count += 1
        else:
            l["is_header"] = False
        
        labeled_lines.append(l)

    # 3. Group into dictionary
    sections = {}
    current_section = "header_info" # Default top section (name, contact, etc)
    sections[current_section] = []

    for l in labeled_lines:
        if l.get("is_header"):
            # Start a new section bucket
            current_section = l["section"]
            sections.setdefault(current_section, [])
        else:
            # Add line to current bucket (entire line object with all info)
            sections.setdefault(current_section, []).append(l)

    return sections