import re

def extract_education_details(lines):
    """
    Extracts College (IIT only), Degree, and Branch from the education section.
    """
    if not lines:
        return {}
        
    # Combine lines into one text block for easier pattern matching
    full_text = "\n".join([l['text'] for l in lines])
    
    edu_data = {
        "college": None,
        "degree": None,
        "branch": None
    }

    # --- 1. Extract College (Restricted to IITs) ---
    # Pattern looks for "IIT <City>" or "Indian Institute of Technology <City>"
    # We capture the word immediately following the IIT text.
    iit_pattern = r"(?:Indian\s*Institute\s*of\s*Technology|IIT)\s*(?:[-–,()]|\s)+([A-Za-z]+)"
    
    match = re.search(iit_pattern, full_text, re.IGNORECASE)
    if match:
        campus = match.group(1).title()
        # Clean up any trailing punctuation just in case
        campus = re.sub(r'[^a-zA-Z]', '', campus)
        edu_data["college"] = f"IIT {campus}"

    # --- 2. Extract Degree ---
    # We prioritize Dual Degree > Masters > Bachelors
    degree_patterns = [
        (r"Dual\s*Degree", "Dual Degree"),
        (r"M\.?\s*Tech", "M.Tech"),
        (r"M\.?\s*E\b", "M.E"),
        (r"M\.?\s*S\b", "M.S"),
        (r"M\.?\s*Sc", "M.Sc"),
        (r"Ph\.?D", "Ph.D"),
        (r"B\.?\s*Tech", "B.Tech"),
        (r"B\.?\s*E\b", "B.E"),
        (r"B\.?\s*S\b", "B.S"),
        (r"B\.?\s*Sc", "B.Sc"),
        # Fallbacks
        (r"Bachelor", "B.Tech"), 
        (r"Master", "M.Tech")
    ]
    
    for pattern, normalized in degree_patterns:
        if re.search(pattern, full_text, re.IGNORECASE):
            edu_data["degree"] = normalized
            break

    # --- 3. Extract Branch ---
    # Strategy: Remove "Minor" info first to avoid confusion
    # e.g. "Major: Electrical, Minor: Computer Science" -> We want Electrical.
    
    text_no_minors = re.sub(r"Minor\s*(?:in|:)?\s*[\w\s]+", "", full_text, flags=re.IGNORECASE)
    
    # Dictionary of Branch Name -> List of Regex Patterns
    branches = {
        "Computer Science": [r"computer\s*science", r"\bcse\b", r"\bcs\b"],
        "Electrical": [r"electrical", r"\beee\b", r"\bece\b", r"electronics"],
        "Mechanical": [r"mechanical", r"\bmech\b"],
        "Civil": [r"civil"],
        "Chemical": [r"chemical"],
        "Aerospace": [r"aerospace"],
        "Engineering Physics": [r"engineering\s*physics", r"\bep\b"],
        "Metallurgical": [r"metallurg", r"material\s*science"],
        "Mathematics": [r"mathematics", r"\bmnc\b", r"computing"],
        "Bioscience": [r"bio", r"biotech"],
        "Data Science": [r"data\s*science", r"\bds\b", r"\bai\b"],
        "Energy": [r"energy"]
    }
    
    for branch_name, regex_list in branches.items():
        found = False
        for regex in regex_list:
            if re.search(regex, text_no_minors, re.IGNORECASE):
                edu_data["branch"] = branch_name
                found = True
                break
        if found:
            break

    return edu_data