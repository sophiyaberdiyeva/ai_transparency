# Code written in co-authorship with Claude Sonnet 4

import os
import shutil
from pathlib import Path
from pdf2image import convert_from_path

def clean_filename(filename):
    """
    Clean filename by removing/replacing problematic characters
    """
    import re
    # Replace non-ASCII characters with underscores
    cleaned = re.sub(r'[^\x00-\x7F]+', '_', filename)
    # Remove multiple consecutive underscores
    cleaned = re.sub(r'_+', '_', cleaned)
    # Remove leading/trailing underscores
    cleaned = cleaned.strip('_')
    return cleaned if cleaned else 'converted_pdf'

def process_zotero_exports(root_folder):
    """
    Process Zotero exported folders:
    1. Remove folders containing non-PDF files
    2. Convert remaining PDFs to PNG images
    
    Args:
        root_folder (str): Path to the main folder containing numbered subfolders
    """
    root_path = Path(root_folder)
    
    if not root_path.exists():
        print(f"Error: Root folder '{root_folder}' does not exist")
        return
    
    # Get all subdirectories (numbered folders)
    subdirs = [d for d in root_path.iterdir() if d.is_dir()]
    
    print(f"Found {len(subdirs)} subdirectories to process")
    
    folders_removed = 0
    pdfs_converted = 0
    
    for subdir in subdirs:
        print(f"\nProcessing folder: {subdir.name}")
        
        # Get all files in the subdirectory
        files = [f for f in subdir.iterdir() if f.is_file()]
        
        if not files:
            print(f"  - Empty folder, skipping")
            continue
        
        if len(files) > 1:
            print(f"  - Multiple files found, expected only 1")
            continue
        
        file_path = files[0]
        file_extension = file_path.suffix.lower()
        
        # Check if file is PDF
        if file_extension != '.pdf':
            print(f"  - Non-PDF file found: {file_path.name}")
            try:
                shutil.rmtree(subdir)
                print(f"  - Removed folder: {subdir.name}")
                folders_removed += 1
            except Exception as e:
                print(f"  - Error removing folder: {e}")
        else:
            # Process PDF
            pdf_name = file_path.stem  # filename without extension
            print(f"  - PDF found: {file_path.name}")
            
            # Handle Cyrillic/non-ASCII characters in filename
            success = False
            
            # Method 1: Try direct conversion first
            try:
                convert_from_path(
                    str(file_path),
                    dpi=500,
                    output_folder=str(subdir),
                    fmt='png',
                    output_file=f'{pdf_name}_'
                )
                print(f"  - Successfully converted to PNG: {pdf_name}")
                pdfs_converted += 1
                success = True
                
            except Exception as e:
                print(f"  - Direct conversion failed: {e}")
            
            # Method 2: Rename file temporarily if direct method failed
            if not success:
                try:
                    # Create ASCII-only temporary filename
                    temp_name = f"temp_pdf_{subdir.name}.pdf"
                    temp_pdf_path = subdir / temp_name
                    
                    # Rename original file temporarily
                    file_path.rename(temp_pdf_path)
                    
                    # Convert with ASCII filename, but use original name for output
                    convert_from_path(
                        str(temp_pdf_path),
                        dpi=500,
                        output_folder=str(subdir),
                        fmt='png',
                        output_file=f'{pdf_name}_'
                    )
                    
                    # Rename back to original
                    temp_pdf_path.rename(file_path)
                    
                    print(f"  - Successfully converted to PNG via temp rename: {pdf_name}")
                    pdfs_converted += 1
                    
                except Exception as e2:
                    print(f"  - Temp rename conversion also failed: {e2}")
                    # Try to rename back if something went wrong
                    try:
                        if temp_pdf_path.exists():
                            temp_pdf_path.rename(file_path)
                    except:
                        pass
    
    print(f"\n=== Summary ===")
    print(f"Folders removed (non-PDF): {folders_removed}")
    print(f"PDFs converted to PNG: {pdfs_converted}")

def main():
    # Example usage
    root_folder = input("Enter the path to your Zotero export folder: ").strip()
    
    # Remove quotes if user copied path with quotes
    root_folder = root_folder.strip('"\'')
    
    if not root_folder:
        print("No folder path provided")
        return
    
    try:
        process_zotero_exports(root_folder)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()