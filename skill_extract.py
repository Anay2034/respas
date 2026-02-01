import re
from skill_data import SKILL_DB

def extract_skills(section_lines):
    """
    Extracts skills from a list of text lines based on SKILL_DB.
    Returns a dictionary grouped by category.
    """
    if not section_lines:
        return {}

    # Combine all lines into one lowercase string for searching
    # We use a set for the found skills to avoid duplicates (e.g. finding "Python" twice)
    full_text = " ".join([l['text'] if isinstance(l, dict) else str(l) for l in section_lines]).lower()
    
    extracted_skills = {}

    for category, skills_map in SKILL_DB.items():
        found_in_category = set()
        
        for skill_name, patterns in skills_map.items():
            for pattern in patterns:
                # Use re.IGNORECASE just to be safe, though text is already lowered
                # We check the pattern against the full text
                if re.search(pattern, full_text, re.IGNORECASE):
                    found_in_category.add(skill_name)
                    # Break loop once skill is found (don't need to match alias if main name matched)
                    break
        
        if found_in_category:
            extracted_skills[category] = list(found_in_category)

    return extracted_skills