import re
from rank_data import EXAM_PATTERNS, RANK_INDICATORS

def split_into_clauses(text):
    """
    Splits a complex sentence into smaller logical chunks.
    CRITICAL CHANGE: Removed comma (,) and brackets () from splitters.
    Splitting on commas breaks lines like "JEE Advanced, AIR 5".
    """
    # Only split on strong delimiters like semicolons, pipes, or explicit 'and'
    # We keep parens () and commas , to preserve context like "JEE (Adv)" or "1,500"
    temp = re.sub(r'[;|]|\s+and\s+', ' <SEP> ', text, flags=re.IGNORECASE)
    chunks = temp.split(' <SEP> ')
    return [c.strip() for c in chunks if c.strip()]

def extract_ranks_from_line(line_text):
    """
    Finds exams and their associated ranks in a single line of text.
    """
    found_ranks = []
    
    # Use original text case but enable case-insensitive matching
    clauses = split_into_clauses(line_text)
    
    # Define local robust indicators to ensure "All India Rank" is prioritized
    # even if rank_data.py is missing it or has a different order.
    ROBUST_INDICATORS = list(set(RANK_INDICATORS + [
        "All India Rank", "AIR", "Secured Rank", "Secured an All India Rank", 
        "Global Rank", "International Rank", "State Rank"
    ]))
    
    # Sort indicators by length (descending) so "All India Rank" matches before "Rank"
    sorted_indicators = sorted(ROBUST_INDICATORS, key=len, reverse=True)
    rank_pattern_str = "|".join([re.escape(i) for i in sorted_indicators])
    
    # Regex for separator: allows "of", ":", "-", whitespace, etc.
    # Added em-dash (—) and 'with'
    separator_pattern = r"[\W\s]*(?:of|is|:|–|-|—|with)?[\W\s]*"
    
    for clause in clauses:
        for exam_name, patterns in EXAM_PATTERNS.items():
            for exam_pat in patterns:
                # 1. Quick check: Is the exam mentioned in this clause?
                if re.search(exam_pat, clause, re.IGNORECASE):
                    
                    # Pattern A: Exam ... Rank ... Number
                    # e.g. "JEE Advanced: AIR 505" or "JEE Advanced Rank 505"
                    p1 = rf"({exam_pat}).*?({rank_pattern_str}){separator_pattern}([\d,]+(?:\.\d+)?)"
                    
                    # Pattern B: Rank ... Number ... Exam
                    # e.g. "Secured AIR 505 in JEE Advanced"
                    p2 = rf"({rank_pattern_str}){separator_pattern}([\d,]+(?:\.\d+)?).*?({exam_pat})"
                    
                    raw_num = None
                    
                    # Try Pattern A
                    m1 = re.search(p1, clause, re.IGNORECASE)
                    if m1:
                        raw_num = m1.group(3)
                    
                    # Try Pattern B (if A failed)
                    if not raw_num:
                        m2 = re.search(p2, clause, re.IGNORECASE)
                        if m2:
                            raw_num = m2.group(2)
                            
                    if raw_num:
                        # Clean the number (remove commas from "1,200")
                        clean_rank = raw_num.replace(',', '')
                        
                        found_ranks.append({
                            "exam": exam_name,
                            "rank": clean_rank,
                            "context": clause
                        })
                        # Break inner loop to avoid double-counting same exam in same clause
                        break 
                        
    return found_ranks

def extract_ranks(section_lines):
    all_ranks = []
    for line in section_lines:
        text = line['text'] if isinstance(line, dict) else str(line)
        ranks_in_line = extract_ranks_from_line(text)
        all_ranks.extend(ranks_in_line)
    return all_ranks