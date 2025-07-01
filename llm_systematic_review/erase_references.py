# -*- coding: utf-8 -*-
# Code written in co-authorship with Claude Sonnet 4
import os
import re
from pathlib import Path

def find_references_section(text):
    """
    Find the start of the References section and identify sections that should be preserved after it.
    
    Returns:
        tuple: (references_start_pos, preserve_sections_text)
    """
    
    # References section headers (case-insensitive)
    references_patterns = [
        r'\b(?:References|Sources|Works Cited|Bibliography|Literature Cited)\b',
        r'\bREFERENCES\b',
        r'\bBIBLIOGRAPHY\b',
        r'\bWORKS CITED\b',
        r'\bSOURCES\b',
        r'\bLITERATURE CITED\b'
    ]
    
    # Sections to preserve after References
    preserve_patterns = [
        r'\b(?:Appendix|Appendices)\b',
        r'\bSupplementary Materials?\b',
        r'\bEthical Approval\b',
        r'\bData Availability Statement\b',
        r'\bCopyright Permissions?\b',
        r'\bErrata\b',
        r'\bCorrections?\b',
        r'\bPatents?\b',
        r'\bCorrespondence Information\b',
        r'\bAPPENDIX\b',
        r'\bAPPENDICES\b',
        r'\bSUPPLEMENTARY MATERIAL\b',
        r'\bETHICAL APPROVAL\b',
        r'\bDATA AVAILABILITY\b',
        r'\bCOPYRIGHT\b',
        r'\bERRATA\b',
        r'\bCORRECTIONS\b',
        r'\bPATENTS\b'
    ]
    
    # Find all potential references section starts
    references_matches = []
    for pattern in references_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
            # Check if this looks like a section header (at start of line or after newline)
            start_pos = match.start()
            if start_pos == 0 or text[start_pos - 1] in '\n\r':
                references_matches.append((start_pos, match.group()))
    
    if not references_matches:
        return None, ""
    
    # Use the first references section found
    references_start = min(references_matches, key=lambda x: x[0])[0]
    
    # Find sections to preserve after references
    preserve_sections = []
    text_after_refs = text[references_start:]
    
    for pattern in preserve_patterns:
        for match in re.finditer(pattern, text_after_refs, re.IGNORECASE | re.MULTILINE):
            start_pos = match.start()
            # Check if this looks like a section header
            if start_pos == 0 or text_after_refs[start_pos - 1] in '\n\r':
                preserve_sections.append((references_start + start_pos, match.group()))
    
    # If we found sections to preserve, extract them
    if preserve_sections:
        # Sort by position
        preserve_sections.sort(key=lambda x: x[0])
        first_preserve_start = preserve_sections[0][0]
        preserve_text = text[first_preserve_start:]
        return references_start, preserve_text
    
    return references_start, ""

def trim_references_from_file(file_path):
    """
    Remove the References section from a text file while preserving important sections.
    
    Args:
        file_path (str): Path to the OCR text file
    
    Returns:
        bool: True if file was modified, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        references_start, preserve_text = find_references_section(content)
        
        if references_start is None:
            print(f"No references section found in {file_path}")
            return False
        
        # Create new content: everything before references + preserved sections
        new_content = content[:references_start].rstrip()
        
        if preserve_text:
            new_content += "\n\n" + preserve_text
            print(f"Trimmed references from {file_path} (preserved post-reference sections)")
        else:
            print(f"Trimmed references from {file_path} (no post-reference sections found)")
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def process_article_folders(root_directory):
    """
    Process all article folders in the root directory.
    
    Args:
        root_directory (str): Path to the directory containing article folders
    """
    root_path = Path(root_directory)
    
    processed_count = 0
    modified_count = 0
    
    # Iterate through all subdirectories
    for folder_path in root_path.iterdir():
        if folder_path.is_dir():
            # Look for OCR text file in this folder
            ocr_files = list(folder_path.glob("*_ocr.txt"))
            
            if len(ocr_files) == 1:
                ocr_file = ocr_files[0]
                print(f"\nProcessing folder: {folder_path.name}")
                print(f"Found OCR file: {ocr_file.name}")
                
                if trim_references_from_file(str(ocr_file)):
                    modified_count += 1
                processed_count += 1
                
    print(f"\n=== Processing Complete ===")
    print(f"Folders processed: {processed_count}")
    print(f"Files modified: {modified_count}")

def main():
    """
    Main function to run the script.
    """
    root_directory = 'data/test_conversion/PDF'
    
    process_article_folders(root_directory)

if __name__ == "__main__":
    main()