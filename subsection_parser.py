from collections import Counter
import re

def get_local_stats(lines):
    """
    Calculates the most common font size and name within a specific section.
    """
    if not lines:
        return 10.0, "Unknown"
        
    sizes = [l["font_size"] for l in lines]
    font_names = [l["font_name"] for l in lines if l.get("font_name")]
    
    local_size = Counter(sizes).most_common(1)[0][0] if sizes else 10.0
    local_font = Counter(font_names).most_common(1)[0][0] if font_names else None
    
    return local_size, local_font

def is_date_line(text):
    """
    Returns True if the line is primarily composed of date-like patterns.
    e.g., 'June 2020 - Present', '2019-2023', 'Summer 2021'
    """
    # Simple heuristic: matches years (19xx, 20xx) or months
    date_pattern = r'\b(19|20)\d{2}\b|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b|present'
    matches = re.findall(date_pattern, text.lower())
    
    # If we find 2+ date components or the text is very short and contains a date
    if len(matches) >= 2:
        return True
    if len(matches) >= 1 and len(text.split()) < 4:
        return True
    return False

def is_bullet_point(text):
    """
    Checks if the line starts with a common bullet character.
    """
    bullets = ["•", "·", "-", "*", "o", "➢", "▪", "‣"]
    clean = text.strip()
    if not clean:
        return False
    return clean[0] in bullets

def is_subsection_header(line, prev_line, local_stats, all_lines=None, current_idx=None):
    """
    Determines if a line is a Subsection Header (e.g., Job Title, Project Name).
    Returns a tuple: (is_header, total_score, score_breakdown_dict)
    """
    local_size, local_font = local_stats
    score = 0
    text = line["text"]
    breakdown = {}
    
    # --- NEGATIVE FILTERS (The "Hard" Logic) ---
    
    # 1. Bullet points are NEVER headers
    if is_bullet_point(text):
        return False, 0, {}

    # 2. Dates are metadata, not headers
    if is_date_line(text):
        return False, 0, {}

    # --- POSITIVE SCORING ---

    # 1. Font Size (Relative to section body)
    if line["font_size"] > local_size: 
        score += 2
        breakdown["font_size"] = 2
    
    # 2. Boldness
    if line.get("bold_ratio", 0) > 0.8:
        score += 2
        breakdown["boldness"] = 2
    elif line.get("bold_ratio", 0) > 0.5:
        score += 1
        breakdown["boldness"] = 1
    
    # 3. Font Change (Contextual)
    # If font matches the section body, it's likely content. If distinct, likely header.
    if local_font and line.get("font_name") != local_font:
        score += 1
        breakdown["font_change"] = 1
    
    # 4. Vertical Spacing (The "Gap" Logic)
    # Headers usually have more space above them than normal lines
    if prev_line:
        raw_gap = abs(prev_line["y"] - line["y"])
        if raw_gap > line["font_size"] * 1.5:
             score += 1
             breakdown["vertical_spacing"] = 1

    # 5. Uppercase check
    if text.isupper() and len(text.split()) < 10:
        score += 1
        breakdown["uppercase"] = 1

    # 6. First line in section (first content item after section header)
    if current_idx == 0:
        score += 1
        breakdown["first_in_section"] = 1

    # 7. Date between section and this line (dates often precede job/project titles)
    if all_lines and current_idx is not None:
        # Look back to find if there's a date between this line and the last section header
        found_date = False
        for i in range(current_idx - 1, -1, -1):
            if all_lines[i].get("is_header"):
                break  # Stop at section header
            if is_date_line(all_lines[i].get("text", "")):
                found_date = True
                break
        if found_date:
            score += 1
            breakdown["date_proximity"] = 1

    # --- DECISION ---
    # We require a higher threshold now.
    return score >= 3, score, breakdown

def extract_subsections(section_lines):
    """
    Groups lines into subsections based on detected headers.
    """
    if not section_lines:
        return []

    local_stats = get_local_stats(section_lines)
    subsections = []
    
    current_sub = None
    intro_lines = []
    
    prev_line = None

    for i, line in enumerate(section_lines):
        # Pass previous line for gap analysis
        prev_line = section_lines[i-1] if i > 0 else None
        
        is_header, total_score, breakdown = is_subsection_header(line, prev_line, local_stats, section_lines, i)
        
        if is_header:
            # Save previous subsection
            if current_sub:
                subsections.append(current_sub)
            
            # Start new subsection
            current_sub = {
                "title": line["text"],
                "line_index": i,
                "score": total_score,
                "score_breakdown": breakdown,
                "content": [] 
            }
        else:
            if current_sub:
                current_sub["content"].append(line)
            else:
                intro_lines.append(line)

    # Append the last one
    if current_sub:
        subsections.append(current_sub)
    
    # Handle intro text (text before first header)
    if intro_lines:
        if not subsections:
             # Case: The whole section has NO headers
             subsections.append({
                 "title": "Summary",
                 "line_index": 0,
                 "score": 0,
                 "score_breakdown": {},
                 "content": intro_lines
             })
        else:
             # Case: Intro text before first job title
             subsections.insert(0, {
                 "title": "Intro",
                 "line_index": 0,
                 "score": 0,
                 "score_breakdown": {},
                 "content": intro_lines
             })

    return subsections