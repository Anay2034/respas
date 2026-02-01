from pdf_processor import extract_lines_from_pdf
from extract_contact import extract_contacts
import json

def add_contact_sources(all_lines, contacts):
    """
    Maps extracted contacts back to their source lines.
    Returns contacts with source information.
    """
    contacts_with_sources = {
        "email": {"value": contacts.get("email"), "source": None},
        "phone": {"value": contacts.get("phone"), "source": None},
        "linkedin": {"value": contacts.get("linkedin"), "source": None},
        "github": {"value": contacts.get("github"), "source": None},
        "portfolio": {"value": contacts.get("portfolio"), "source": None}
    }
    
    # Scan header area (top 30 lines)
    header_scope = all_lines[:30]
    
    for idx, line in enumerate(header_scope):
        text = line['text']
        links = line.get('links', [])
        
        # Find which contact appears in this line
        for contact_type, contact_value in contacts.items():
            if contact_value and contact_type in contacts_with_sources:
                if contact_value in text or contact_value.replace("https://www.", "") in text:
                    if not contacts_with_sources[contact_type]['source']:
                        contacts_with_sources[contact_type]['source'] = {
                            "line_index": idx,
                            "text": text,
                            "method": "regex_text"
                        }
                
                # Check links
                for link in links:
                    # Handle link as dict or string
                    link_uri = link.get('uri') if isinstance(link, dict) else link
                    
                    if link_uri and (contact_value in link_uri or link_uri in contact_value):
                        if not contacts_with_sources[contact_type]['source']:
                            contacts_with_sources[contact_type]['source'] = {
                                "line_index": idx,
                                "text": text,
                                "method": "pdf_link",
                                "uri": link_uri
                            }
    
    return contacts_with_sources

def main():
    pdf_filename = "rizzume.pdf"
    
    print(f"Processing {pdf_filename}...")
    
    # 1. Extract lines from PDF
    raw_lines = extract_lines_from_pdf(pdf_filename)
    
    if not raw_lines:
        print("No text found in PDF.")
        return
    
    # 2. Extract contacts using extract_contact.py
    contacts = extract_contacts(raw_lines)
    
    # 3. Add source information
    contacts_with_sources = add_contact_sources(raw_lines, contacts)
    
    # 4. Build output data
    output_data = {
        "pdf_file": pdf_filename,
        "contacts": contacts_with_sources,
        "summary": {
            "total_lines_scanned": min(30, len(raw_lines)),
            "emails_found": 1 if contacts_with_sources['email']['value'] else 0,
            "phones_found": 1 if contacts_with_sources['phone']['value'] else 0,
            "linkedin_found": 1 if contacts_with_sources['linkedin']['value'] else 0,
            "github_found": 1 if contacts_with_sources['github']['value'] else 0,
        }
    }
    
    # 5. Save to contacts.json
    with open("contacts.json", "w") as f:
        json.dump(output_data, f, indent=4, default=str)
    
    print("Results saved to contacts.json")
    print(f"\nFound Contacts:")
    for contact_type, info in contacts_with_sources.items():
        print(f"  {contact_type.upper()}: {info['value']}")

if __name__ == "__main__":
    main()