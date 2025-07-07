#Code written in coauthorship with Gemini Pro

import os
import re
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from PIL import Image

# --- Configuration ---
# Set the path to the Tesseract executable.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def beautify_text(text: str):
    """
    Removes unnecessary line breaks and extra spaces from the text.
    It attempts to rejoin paragraphs that were split across lines,
    including words that were hyphenated.
    
    Args:
        text (str): The raw extracted text.

    Returns:
        str: The beautified text.
    """
    # 1. Handle lines ending with double spaces followed by line breaks
    # Convert double spaces at line end to single space and join with next line
    text = re.sub(r'  \n([a-zA-Z0-9\-–—])', r' \1', text)
    
    # 2. Rejoin words that were hyphenated across lines with space after syllable
    # (e.g., "so -\nme" -> "some")
    text = re.sub(r'(\w+) -\n(\w+)', r'\1\2', text)
    
    # 3. Rejoin words that were hyphenated with hyphen on separate line
    # (e.g., "ad\n-\ndress" -> "address")
    text = re.sub(r'(\w+)\n-\n(\w+)', r'\1\2', text)
    
    # 4. Rejoin words that were hyphenated across lines without space
    # (e.g., "so-\nme" -> "some")
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    
    # 5. Replace multiple newlines with just two, to standardize paragraph breaks
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # 6. Join lines that are likely part of the same paragraph.
    # This looks for a line ending in a lowercase letter, comma, or parentheses, followed
    # by a newline and another letter/digit/dash, and replaces the newline with a space.
    text = re.sub(r'([a-z,0-9\(\)<>:\'\”=])\n([\(\)-–—=a-zA-Z0-9])', r'\1 \2', text)
    
    # 7. Remove line breaks after paragraphs that end with whitespace
    # (but keep the whitespace itself)
    text = re.sub(r'(\s)\n([a-zA-Z0-9\-–—=])', r'\1\2', text)
    
    # Correct common OCR misrecognition: 'Al' (as in Artificial Intelligence) → 'AI'
    text = re.sub(r'\bAl\b', 'AI', text)
    
    return text.strip()


def extract_text_from_pdf(pdf_path: str):
    """
    Extracts text from a PDF file using OCR. All PDFs are treated as image-based
    and processed through OCR for consistent text extraction.
    
    Args:
        pdf_path (str): The full path to the PDF file.

    Returns:
        str: The extracted and cleaned text.
    """
    text = ""
    try:
        print(f"Processing '{os.path.basename(pdf_path)}' with OCR...")
        text = ocr_from_pdf(pdf_path)
        
        if not text.strip():
            print(f"No text could be extracted from '{os.path.basename(pdf_path)}'.")
            
    except Exception as e:
        print(f"OCR failed for '{os.path.basename(pdf_path)}'. Error: {e}")
        text = "" # Start with empty text if OCR fails

    # Beautify the extracted text
    beautified_text = beautify_text(text)
    
    return beautified_text

def ocr_from_pdf(pdf_path):
    """
    Performs OCR on a PDF file to extract text. This is used for PDFs
    that contain images of text rather than selectable text.

    Args:
        pdf_path (str): The full path to the PDF file.

    Returns:
        str: The text extracted using OCR.
    """
    ocr_text = ""
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            print(f"  - OCR on page {i+1} of '{os.path.basename(pdf_path)}'")
            # Use Tesseract to do OCR on the image
            ocr_text += pytesseract.image_to_string(image) + "\n"
    except Exception as e:
        print(f"An error occurred during OCR processing for '{os.path.basename(pdf_path)}': {e}")
    return ocr_text

def process_folders(root_folder):
    """
    Iterates through all subfolders of a given root folder, finds PDF files,
    extracts their text and tables, and saves it to a .txt file.
    """
    print(f"Starting to process folders inside '{root_folder}'...")

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                pdf_full_path = os.path.join(dirpath, filename)

                txt_filename = os.path.splitext(filename)[0] + '.txt'
                txt_full_path = os.path.join(dirpath, txt_filename)

                extracted_content = extract_text_from_pdf(pdf_full_path)

                if extracted_content.strip():
                    try:
                        with open(txt_full_path, 'w', encoding='utf-8') as txt_file:
                            txt_file.write(extracted_content)
                        print(f"Successfully saved content to '{txt_filename}'")
                    except IOError as e:
                        print(f"Error writing to file '{txt_full_path}'. Error: {e}")
                else:
                    print(f"No content could be extracted from '{filename}'. No .txt file created.")

    print("\nProcessing complete.")

if __name__ == '__main__':
    folder_to_process = 'C:/Users/Admin/Documents/Max Planck ARC/AI persuasion/ai_transparency/data/test_conversion/PDF'
    process_folders(folder_to_process)
    