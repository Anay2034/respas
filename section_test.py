from pdf_processor import extract_lines_from_pdf
from section_parser import process_lines_to_sections
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
    
    # 3. Print Results
    print("\n" + "="*40)
    print(f"PARSED SECTIONS FOR: {pdf_filename}")
    print("="*40)

    for section_name, content in sections.items():
        print(f"\n--- {section_name.upper()} ---")
        if not content:
            print("  [Empty Section]")
        else:
            for line in content:
                print(f"  • {line}")
    
    # Optional: Save to JSON to see the structure
    with open("output.json", "w") as f:
        json.dump(sections, f, indent=4)

if __name__ == "__main__":
    main()