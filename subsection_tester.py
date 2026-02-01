from pdf_processor import extract_lines_from_pdf
from section_parser import process_lines_to_sections
from subsection_parser import extract_subsections
import json

def main():
    # Replace this with your actual PDF filename
    pdf_filename = "ankeet.pdf" 
    
    print(f"Processing {pdf_filename}...")
    
    # 1. Extract raw data
    raw_lines = extract_lines_from_pdf(pdf_filename)
    
    if not raw_lines:
        print("No text found in PDF.")
        return

    # 2. Convert to sections
    sections = process_lines_to_sections(raw_lines)
    
    # 3. Build output structure
    output_data = {}
    
    for section_name, lines_list in sections.items():
        # Extract the section keyword (first word before the hyphen)
        section_keyword = section_name.split('-')[0] if '-' in section_name else section_name
        
        # Apply Subsection Logic for specific sections
        if section_keyword in ["experience", "positions", "projects"]:
            subsections = extract_subsections(lines_list)
            output_data[section_name] = subsections
        else:
            # Keep raw line objects for other sections
            output_data[section_name] = lines_list
    
    # 4. Save to output.json
    with open("output.json", "w") as f:
        json.dump(output_data, f, indent=4, default=str)
    
    print(f"Results saved to output.json")

if __name__ == "__main__":
    main()