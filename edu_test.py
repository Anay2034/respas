from pdf_processor import extract_lines_from_pdf
from section_parser import process_lines_to_sections
from extract_edu import extract_education_details
import json

def main():
    # Replace this with your actual PDF filename
    pdf_filename = "hardik.pdf"
    
    print(f"Processing {pdf_filename}...")
    
    # 1. Extract raw data from PDF
    raw_lines = extract_lines_from_pdf(pdf_filename)
    
    if not raw_lines:
        print("No text found in PDF.")
        return
    
    # 2. Convert to sections
    sections = process_lines_to_sections(raw_lines)
    
    # 3. Build output structure for education sections
    output_data = {}
    
    for section_name, lines_list in sections.items():
        # Extract the section keyword (first word before the hyphen)
        section_keyword = section_name.split('-')[0] if '-' in section_name else section_name
        
        # Only process education sections
        if section_keyword == "education":
            # Extract education details
            edu_details = extract_education_details(lines_list)
            
            # Create entry with original lines and extracted details
            output_data[section_name] = {
                "lines": lines_list,  # Original education section lines
                "extracted": edu_details  # Extracted education info
            }
    
    # 4. Save to education.json
    with open("education.json", "w") as f:
        json.dump(output_data, f, indent=4, default=str)
    
    print(f"Results saved to education.json")
    print(f"Processed {len(output_data)} education section(s)")
    
    # Print extracted details
    for section_name, data in output_data.items():
        print(f"\n[{section_name}]")
        edu = data['extracted']
        print(f"  College: {edu.get('college')}")
        print(f"  Degree: {edu.get('degree')}")
        print(f"  Branch: {edu.get('branch')}")

if __name__ == "__main__":
    main()
