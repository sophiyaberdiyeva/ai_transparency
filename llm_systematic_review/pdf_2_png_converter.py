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
            original_pdf_path = file_path  # save reference to original path
            print(f"  - PDF found: {file_path.name}")
            
            try:
                # Create ASCII-only temporary filename
                temp_name = f"temp_pdf_{subdir.name}.pdf"
                temp_pdf_path = subdir / temp_name
                
                # Rename original file temporarily to ASCII-only name
                original_pdf_path.rename(temp_pdf_path)
                print(f"  - Temporarily renamed to: {temp_name}")
                
                # Convert with ASCII filename, but use original name for output
                convert_from_path(
                    str(temp_pdf_path),
                    dpi=500,
                    output_folder=str(subdir),
                    fmt='png',
                    output_file=f'{pdf_name}_'
                )
                
                # Rename back to original
                temp_pdf_path.rename(original_pdf_path)
                print(f"  - Renamed back to original name")
                
                print(f"  - Successfully converted to PNG: {pdf_name}")
                pdfs_converted += 1
                
            except Exception as e:
                print(f"  - Error converting PDF: {e}")
                # Try to rename back if something went wrong
                try:
                    if temp_pdf_path.exists():
                        temp_pdf_path.rename(original_pdf_path)
                        print(f"  - Restored original filename after error")
                except Exception as restore_error:
                    print(f"  - Failed to restore original filename: {restore_error}")
    
    print(f"\n=== Summary ===")
    print(f"Folders removed (non-PDF): {folders_removed}")
    print(f"PDFs converted to PNG: {pdfs_converted}")


def main():
    # Usage from user input
    #root_folder = input("Enter the path to your Zotero export 'PDF' folder: ").strip()
    
    root_folder = 'data/test_conversion/PDF'
    
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