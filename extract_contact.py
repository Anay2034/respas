import re

def extract_contacts(all_lines):
    """
    Scans the entire document (or header section) for contact details.
    Uses regex on text AND checks hidden PDF hyperlinks.
    """
    contacts = {
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "portfolio": None
    }
    
    # Regex Patterns
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Phone Pattern: 5-5 (India), 3-3-4 (US), or Continuous
    phone_pattern = r'(?:\+?\d{1,3}[ -]?)?(?:\d{5}[ -]?\d{5}|\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4}|\d{10,12})'
    
    # Scan header area (first 30 lines)
    header_scope = all_lines[:30] 
    
    for line in header_scope:
        text = line['text']
        
        # Get the list of links (defaults to empty list)
        # These are STRINGS, e.g. ["https://linkedin.com/...", "mailto:..."]
        hidden_links = line.get('links', []) 
        
        # 1. Email Extraction
        if not contacts['email']:
            match = re.search(email_pattern, text)
            if match:
                contacts['email'] = match.group()
            
            # Check hidden links for mailto
            for link in hidden_links:
                # 'link' is a string, so we check it directly
                if "mailto:" in link.lower():
                    # Clean potential query params (e.g. ?subject=...) and prefix
                    clean_link = link.split('?')[0]
                    contacts['email'] = re.sub(r'mailto:', '', clean_link, flags=re.IGNORECASE)
                    break

        # 2. Phone Extraction
        if not contacts['phone']:
            match = re.search(phone_pattern, text)
            if match:
                phone_candidate = match.group()
                digits_only = re.sub(r'\D', '', phone_candidate)
                # Filter out years like 2020-2024 (starts with 19/20 and is 8 chars long)
                if not (len(digits_only) == 8 and (digits_only.startswith("20") or digits_only.startswith("19"))):
                     contacts['phone'] = phone_candidate.strip()

        # 3. LinkedIn Extraction
        if not contacts['linkedin']:
            # Visible Text
            if "linkedin.com" in text.lower():
                match = re.search(r'linkedin\.com/in/[a-zA-Z0-9_-]+', text, re.IGNORECASE)
                if match:
                    contacts['linkedin'] = "https://www." + match.group()
            
            # Hidden Links
            for link in hidden_links:
                if "linkedin.com" in link.lower():
                    # Strip any query parameters
                    contacts['linkedin'] = link.split('?')[0]
                    break

        # 4. GitHub Extraction
        if not contacts['github']:
            # Visible Text
            if "github.com" in text.lower():
                match = re.search(r'github\.com/[a-zA-Z0-9_-]+', text, re.IGNORECASE)
                if match:
                    contacts['github'] = "https://www." + match.group()
            
            # Hidden Links
            for link in hidden_links:
                if "github.com" in link.lower():
                    contacts['github'] = link.split('?')[0]
                    break

    return contacts