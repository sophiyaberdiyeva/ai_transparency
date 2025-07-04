import os
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from PIL import Image

# --- Configuration ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file. It first tries to extract text directly.
    If that fails or returns very little text, it assumes the PDF is an image
    and uses OCR to extract the text.

    Args:
        pdf_path (str): The full path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        # Try to extract text directly from the PDF
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        # If the extracted text is very short, it might be an image-based PDF
        if len(text.strip()) < 100:
            print(f"'{os.path.basename(pdf_path)}' seems to be image-based. Trying OCR...")
            text = ocr_from_pdf(pdf_path)

    except Exception as e:
        print(f"Could not read text directly from '{os.path.basename(pdf_path)}'. Error: {e}")
        print("Attempting OCR as a fallback.")
        try:
            text = ocr_from_pdf(pdf_path)
        except Exception as ocr_e:
            print(f"OCR also failed for '{os.path.basename(pdf_path)}'. Error: {ocr_e}")
            return "" # Return empty string if both methods fail

    return text

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
    extracts their text, and saves it to a .txt file in the same subfolder.

    Args:
        root_folder (str): The path to the main folder to start processing from.
    """
    if not os.path.isdir(root_folder):
        print(f"Error: The folder '{root_folder}' does not exist.")
        return

    print(f"Starting to process folders inside '{root_folder}'...")

    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(root_folder):
        print(f"\nScanning folder: '{dirpath}'")
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                pdf_full_path = os.path.join(dirpath, filename)
                print(f"Found PDF: '{filename}'")

                # Define the output text file path
                txt_filename = os.path.splitext(filename)[0] + '.txt'
                txt_full_path = os.path.join(dirpath, txt_filename)

                # Extract text from the PDF
                extracted_text = extract_text_from_pdf(pdf_full_path)

                if extracted_text.strip():
                    # Write the extracted text to a .txt file
                    try:
                        with open(txt_full_path, 'w', encoding='utf-8') as txt_file:
                            txt_file.write(extracted_text)
                        print(f"Successfully saved text to '{txt_filename}'")
                    except IOError as e:
                        print(f"Error writing to file '{txt_full_path}'. Error: {e}")
                else:
                    print(f"No text could be extracted from '{filename}'. No .txt file created.")

    print("\nProcessing complete.")

if __name__ == '__main__':
    folder_to_process = 'C:/Users/Admin/Documents/Max Planck ARC/AI persuasion/ai_transparency/data/test_conversion/PDF'
    process_folders(folder_to_process)
    