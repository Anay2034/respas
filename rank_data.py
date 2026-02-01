# Normalized Exam Name -> List of strict regex patterns
# We explicitly separate JEE Advanced and JEE Mains.
EXAM_PATTERNS = {
    "JEE Advanced": [
        r"jee\s*advanced", 
        r"jee\s*adv", 
        r"iit\s*jee",  # Legacy name, usually implies Advanced
        r"iit\s*entrance"
    ],
    "JEE Mains": [
        r"jee\s*mains?", 
        r"aieee",      # Legacy name for Mains
        r"joint\s*entrance\s*examination\s*mains?"
    ],
    "GATE": [r"\bgate\b"], # \b ensures we don't match "gatekeeper"
    "BITSAT": [r"bitsat"],
    "KVPY": [r"kvpy", r"kishore\s*vaigyanik\s*protsahan\s*yojana"],
    "Olympiad": [
        r"olympiad", 
        r"\brmo\b", r"\binmo\b",  # Math Olympiads
        r"\bipho\b", r"\bicho\b", # Physics/Chem Olympiads
        r"\bimo\b"
    ],
    "CET": [r"\bcet\b", r"mh-?cet", r"kcet", r"mht-?cet"],
    "CAT": [r"\bcat\b", r"common\s*admission\s*test"],
    "UPSC": [r"upsc", r"cse", r"civil\s*services"],
    "NTSE": [r"ntse", r"national\s*talent\s*search\s*examination", r"nts\s*scholarship"]
}

# Keywords that indicate a rank. 
# We look for these in proximity to the exam name and number.
RANK_INDICATORS = [
    r"air", 
    r"all\s*india\s*rank", 
    r"rank", 
    r"secured\s*rank", 
    r"standing", 
    r"percentile",
    r"score"  # Added score for GATE/CAT contexts
]