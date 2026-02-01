from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar
from pdfminer.pdfpage import PDFPage
from pdfminer.pdftypes import PDFObjRef
from collections import Counter
import re

def is_font_bold(char, font_name=None):
    """
    Robustly checks if a character is bold based on font attributes.
    """
    try:
        check_font = font_name.lower() if font_name else char.fontname.lower()
        bold_indicators = ["bold", "black", "heavy", "bd", "demi", "bx"]
        
        if any(indicator in check_font for indicator in bold_indicators):
            return True
            
        if hasattr(char, 'font') and hasattr(char.font, 'descriptor'):
            flags = char.font.descriptor.get('Flags', 0)
            if flags & 262144: 
                return True
    except AttributeError: 
        pass
    return False

def normalize_lines(lines):
    for l in lines:
        l["text"] = re.sub(r'\s+', ' ', l["text"]).strip()
    return lines

def extract_lines_from_pdf(pdf_path):
    """
    Extracts text and merges hyperlinks using an efficient Single-Pass method.
    Returns a list of links for each line to handle multiple URLs (e.g. LinkedIn + GitHub).
    """
    # Setup Layout Analysis
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    all_lines = []

    try:
        with open(pdf_path, 'rb') as fp:
            # Loop through pages EXACTLY ONCE
            for page in PDFPage.get_pages(fp):
                
                # --- A. Extract Links for THIS Page ---
                page_links = []
                if page.annots:
                    annots = page.annots
                    if isinstance(annots, PDFObjRef): annots = annots.resolve()
                    if isinstance(annots, list):
                        for annot in annots:
                            if isinstance(annot, PDFObjRef): annot = annot.resolve()
                            
                            # Filter for Links
                            if annot.get('Subtype') and annot.get('Subtype').name == 'Link':
                                action = annot.get('A')
                                if action and isinstance(action, dict):
                                    uri = action.get('URI')
                                    # REMOVED: uri = action.get('D') to avoid internal page jumps
                                    
                                    if uri:
                                        if isinstance(uri, bytes):
                                            try: uri = uri.decode('utf-8')
                                            except: pass
                                        
                                        rect = annot.get('Rect') # [x0, y0, x1, y1]
                                        if rect:
                                            page_links.append({
                                                'bbox': rect,
                                                'uri': str(uri)
                                            })

                # --- B. Extract Text Layout for THIS Page ---
                interpreter.process_page(page)
                layout = device.get_result()
                
                page_lines = []
                
                # Flatten layout to lines
                text_items = []
                for element in layout:
                    if isinstance(element, LTTextBox):
                        for line in element: text_items.append(line)
                    elif isinstance(element, LTTextLine):
                        text_items.append(element)
                
                # --- C. Process Lines & Check Overlaps ---
                for text_line in text_items:
                    raw_text = text_line.get_text()
                    if not raw_text.strip(): continue

                    # Font Analysis
                    sizes, fonts = [], []
                    bold_chars, total_chars = 0, 0
                    
                    for char in text_line:
                        if isinstance(char, LTChar):
                            sizes.append(char.size)
                            # Clean font name (remove subset tag like ABCDE+)
                            font_name = char.fontname.split('+')[-1] if '+' in char.fontname else char.fontname
                            fonts.append(font_name)
                            total_chars += 1
                            if is_font_bold(char, font_name): bold_chars += 1

                    if not sizes: continue

                    # --- OVERLAP LOGIC ---
                    found_links = []
                    # Text Line Coordinates
                    tx0, ty0, tx1, ty1 = text_line.x0, text_line.y0, text_line.x1, text_line.y1
                    
                    for link in page_links:
                        lx0, ly0, lx1, ly1 = link['bbox']
                        
                        # Check if rectangles overlap
                        # (Left of one < Right of other) AND (Bottom of one < Top of other)
                        if (tx0 < lx1 and tx1 > lx0 and
                            ty0 < ly1 and ty1 > ly0):
                            found_links.append(link['uri'])

                    page_lines.append({
                        "text": raw_text.strip(),
                        "font_size": round(max(sizes), 1),
                        "bold_ratio": bold_chars / max(total_chars, 1),
                        "font_name": Counter(fonts).most_common(1)[0][0] if fonts else "Unknown",
                        "y": text_line.y0,
                        "x": text_line.x0,
                        "links": found_links # <--- CHANGED: Stores all matching links
                    })
                
                # Sort: Top-down, then Left-Right
                page_lines.sort(key=lambda item: (-item["y"], item["x"]))
                all_lines.extend(page_lines)

        return normalize_lines(all_lines)

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []