from pdf_processor import extract_lines_from_pdf
from section_parser import process_lines_to_sections
from rank_extract import extract_ranks
import json

def main():
    # Replace this with your actual PDF filename
    pdf_filename = "rizzume.pdf" 
    
    print(f"Processing {pdf_filename}...")
    
    # 1. Extract raw data
    raw_lines = extract_lines_from_pdf(pdf_filename)
    
    if not raw_lines:
        print("No text found in PDF.")
        return

    # 2. Convert to sections
    sections = process_lines_to_sections(raw_lines)
    
    # 3. Build output structure for achievements with extracted ranks
    output_data = {}
    
    for section_name, lines_list in sections.items():
        # Extract the section keyword (first word before the hyphen)
        section_keyword = section_name.split('-')[0] if '-' in section_name else section_name
        
        # Only process achievement sections
        if section_keyword == "achievements":
            # Extract ranks from the achievement lines
            extracted_ranks = extract_ranks(lines_list)
            
            # Create new dictionary with original section and extracted ranks
            output_data[section_name] = {
                "lines": lines_list,  # Original section lines
                "ranks": extracted_ranks  # Extracted rank information
            }
    
    # 4. Save to rank.json
    with open("rank.json", "w") as f:
        json.dump(output_data, f, indent=4, default=str)
    
    print(f"Results saved to rank.json")
    print(f"Processed {len(output_data)} achievement section(s)")

if __name__ == "__main__":
    main()
