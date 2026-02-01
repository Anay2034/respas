import json
import os

# --- Import Physical & Logical Layers ---
from pdf_processor import extract_lines_from_pdf
from section_parser import process_lines_to_sections
from subsection_parser import extract_subsections

# --- Import Specific Extractors ---
# Ensure these filenames match exactly what you saved
from extract_contact import extract_contacts
from extract_edu import extract_education_details
from rank_extract import extract_ranks
from skill_extract import extract_skills

def main():
    # Replace with your actual PDF filename
    pdf_filename = "ankeet.pdf" 
    
    if not os.path.exists(pdf_filename):
        print(f"Error: File '{pdf_filename}' not found.")
        return

    print(f"Processing {pdf_filename}...")

    # 1. Physical Layer: Extract Raw Lines & Links
    raw_lines = extract_lines_from_pdf(pdf_filename)
    
    if not raw_lines:
        print("No text extracted from PDF.")
        return

    # 2. Logical Layer: Group Lines into Sections
    sections = process_lines_to_sections(raw_lines)

    # 3. Initialize Final Output Structure
    final_output = {
        "extracted": {
            "contact": {},
            "edu": {},
            "rank": [],
            "skill": {}
        },
        "resume": {}
    }

    # --- GLOBAL EXTRACTION (Contact Info) ---
    # Contacts are extracted from the raw lines (usually header area)
    final_output["extracted"]["contact"] = extract_contacts(raw_lines)

    # --- SECTION-SPECIFIC PROCESSING ---
    for section_key, lines_list in sections.items():
        # Identify section type (e.g., "experience-Work Experience" -> "experience")
        # "misc_0" remains "misc_0"
        section_type = section_key.split('-')[0] if '-' in section_key else section_key
        
        # ---------------------------------------------------------
        # A. POPULATE "EXTRACTED" (Structured Data)
        # ---------------------------------------------------------
        
        if section_type == "education":
            # Extract IIT College, Degree, Branch
            edu_info = extract_education_details(lines_list)
            # Update if valid info found
            if edu_info.get("college") or edu_info.get("degree"):
                final_output["extracted"]["edu"].update(edu_info)

        elif section_type == "achievements":
            # Extract Exam Ranks
            ranks = extract_ranks(lines_list)
            final_output["extracted"]["rank"].extend(ranks)

        elif section_type == "skills":
            # Extract Skills using Database
            skills = extract_skills(lines_list)
            # Merge dictionary to handle multiple skill sections if they exist
            for cat, s_list in skills.items():
                if cat in final_output["extracted"]["skill"]:
                    existing = set(final_output["extracted"]["skill"][cat])
                    existing.update(s_list)
                    final_output["extracted"]["skill"][cat] = list(existing)
                else:
                    final_output["extracted"]["skill"][cat] = s_list

        # ---------------------------------------------------------
        # B. POPULATE "RESUME" (Structure & Content)
        # ---------------------------------------------------------
        
        # Apply Subsection Logic ONLY for Experience, Projects, Positions
        if section_type in ["experience", "projects", "positions"]:
            structured_subsections = extract_subsections(lines_list)
            
            # Clean up output: formatted title + list of details (text only)
            clean_content = []
            for sub in structured_subsections:
                clean_content.append({
                    "title": sub.get("title", "Untitled"),
                    "details": [l["text"] for l in sub.get("content", [])]
                })
            
            final_output["resume"][section_key] = clean_content
        
        else:
            # For other sections (Skills, Education, Header, etc.), store simple text list.
            # This preserves the Resume structure without forcing subsections where they don't fit.
            final_output["resume"][section_key] = [l["text"] for l in lines_list]

    # 4. Save to JSON
    output_filename = "parsed_resume.json"
    with open(output_filename, "w") as f:
        json.dump(final_output, f, indent=4)

    print(f"Parsing complete. Data saved to {output_filename}")
    
    # Debug Print
    print("\n--- Extracted Metadata ---")
    print(json.dumps(final_output["extracted"], indent=2))

if __name__ == "__main__":
    main()