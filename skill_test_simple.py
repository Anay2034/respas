import json
from pdf_processor import extract_lines_from_pdf
from section_parser import process_lines_to_sections
from skill_extract import extract_skills


def test_single_pdf(pdf_filename="rizzume.pdf"):
    """
    Simple test function for quick skill extraction testing.
    Uses PDF preprocessing and section parser to extract skills.
    """
    print(f"\n{'='*70}")
    print(f"SKILL EXTRACTION TEST: {pdf_filename}")
    print(f"{'='*70}\n")
    
    # Step 1: Extract raw lines from PDF
    print("[Step 1] Extracting lines from PDF using pdf_processor...")
    raw_lines = extract_lines_from_pdf(pdf_filename)
    print(f"✓ Extracted {len(raw_lines)} lines\n")
    
    # Step 2: Parse into sections using section_parser
    print("[Step 2] Parsing sections using section_parser...")
    sections = process_lines_to_sections(raw_lines)
    print(f"✓ Found {len(sections)} sections:")
    for section_name in sections.keys():
        print(f"   - {section_name}")
    print()
    
    # Step 3: Find skills section
    print("[Step 3] Locating skills section...")
    skills_section = None
    skills_section_name = None
    
    for section_name, content in sections.items():
        if "skill" in section_name.lower():
            skills_section = content
            skills_section_name = section_name
            print(f"✓ Found skills section: '{skills_section_name}'")
            print(f"  Section contains {len(skills_section)} lines")
            print("\n  Section Preview:")
            for i, line in enumerate(skills_section[:10], 1):
                text = line.get('text', str(line)) if isinstance(line, dict) else str(line)
                print(f"    {i}. {text[:70]}")
            if len(skills_section) > 10:
                print(f"    ... and {len(skills_section) - 10} more lines")
            break
    
    if not skills_section:
        print("⚠ No skills section found in standard sections")
        print("Available sections:", list(sections.keys()))
        return None
    
    print()
    
    # Step 4: Extract skills using skill_extract
    print("[Step 4] Extracting skills from section...")
    extracted_skills = extract_skills(skills_section)
    
    # Format results
    results = {
        "pdf_file": pdf_filename,
        "sections_found": list(sections.keys()),
        "skills_section_name": skills_section_name,
        "extracted_skills": extracted_skills,
        "statistics": {
            "total_lines_in_pdf": len(raw_lines),
            "total_sections": len(sections),
            "lines_in_skills_section": len(skills_section),
            "skill_categories_found": len(extracted_skills),
            "total_skills_found": sum(len(v) for v in extracted_skills.values())
        }
    }
    
    # Save results
    output_file = f"skill_results_{pdf_filename.replace('.pdf', '.json')}"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Display results
    print("="*70)
    print("EXTRACTION RESULTS - Skills by Category")
    print("="*70)
    
    if extracted_skills:
        for category, skills in extracted_skills.items():
            print(f"\n{category}:")
            for skill in skills:
                print(f"  ✓ {skill}")
    else:
        print("No skills found")
    
    print("\n" + "="*70)
    print("STATISTICS")
    print("="*70)
    for key, value in results["statistics"].items():
        print(f"{key}: {value}")
    
    print(f"\n✓ Results saved to: {output_file}\n")
    
    return results


if __name__ == "__main__":
    # Test on a specific PDF
    test_single_pdf("rizzume.pdf")
    
    # Uncomment to test on multiple PDFs
    # for pdf in ["ankeet.pdf", "hardik.pdf", "iitb.pdf"]:
    #     try:
    #         test_single_pdf(pdf)
    #         print("\n" + "-"*70 + "\n")
    #     except Exception as e:
    #         print(f"Error processing {pdf}: {e}\n")
