# Code written in co-authorship with Claude Sonnet 4
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
from typing import List, Dict, Optional

def process_scopus_files(file_paths: List[str], output_dir: str = 'output') -> pd.DataFrame:
    """
    Process multiple Scopus HTML files, extract data, and create RIS files.
    
    Args:
        file_paths: List of paths to HTML files to process
        output_dir: Directory to save RIS files
    
    Returns:
        Combined DataFrame with all extracted data
    """
    all_data = []
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for i, file_path in enumerate(file_paths, 1):
        print(f"Processing file {i}/{len(file_paths)}: {file_path}")
        
        try:
            # Read and parse HTML file
            with open(file_path, 'r', encoding='utf-8') as page:
                soup = BeautifulSoup(page.read(), 'html.parser')
            
            # Extract data from current file
            titles = [elem.get_text().strip() for elem in soup.find_all(class_='Typography-module__ETlt8')]
            authors = [elem.get_text().strip() for elem in soup.find_all(class_='author-list')]
            years = [elem.get_text().strip() for elem in soup.find_all(class_='TableItems-module__472S1')]
            abstracts = [elem.get_text().strip() for elem in soup.find_all(class_='Abstract-module__ukTwj')]
            pdf_links = [elem.get('href') for elem in soup.find_all('a') if elem.get_text() and 'View PDF' in elem.get_text()]
            
            # Ensure all lists have the same length by padding with empty strings
            max_len = max(len(titles), len(authors), len(years), len(abstracts), len(pdf_links))
            titles.extend([''] * (max_len - len(titles)))
            authors.extend([''] * (max_len - len(authors)))
            years.extend([''] * (max_len - len(years)))
            abstracts.extend([''] * (max_len - len(abstracts)))
            pdf_links.extend([''] * (max_len - len(pdf_links)))
            
            # Create DataFrame for current file
            file_df = pd.DataFrame({
                'title': titles,
                'author': authors,
                'year': years,
                'abstract': abstracts,
                'pdf_link': pdf_links,
                'source_file': [os.path.basename(file_path)] * max_len
            })
            
            all_data.append(file_df)
            print(f"  Extracted {len(file_df)} records from {file_path}")
            
        except Exception as e:
            print(f"  Error processing {file_path}: {str(e)}")
            continue
    
    # Combine all DataFrames
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"\nTotal records collected: {len(combined_df)}")
        
        # Remove rows where all main fields are empty
        combined_df = combined_df[
            (combined_df['title'] != '') | 
            (combined_df['author'] != '') | 
            (combined_df['abstract'] != '')
        ]
        print(f"Records after cleaning: {len(combined_df)}")
        
        # Generate RIS files
        create_ris_files(combined_df, output_dir)
        
        return combined_df
    else:
        print("No data was extracted from any files.")
        return pd.DataFrame()

def create_ris_files(df: pd.DataFrame, output_dir: str) -> None:
    """
    Create RIS files from the DataFrame.
    
    Args:
        df: DataFrame containing the extracted data
        output_dir: Directory to save RIS files
    """
    # Create a single RIS file with all records
    all_records_file = os.path.join(output_dir, 'all_records.ris')
    
    with open(all_records_file, 'w', encoding='utf-8') as f:
        for idx, row in df.iterrows():
            f.write(format_ris_record(row, idx + 1))
    
    print(f"Created RIS file: {all_records_file}")
    
    # Create separate RIS files by source file
    for source_file in df['source_file'].unique():
        if source_file:
            source_df = df[df['source_file'] == source_file]
            ris_filename = os.path.join(output_dir, f"{os.path.splitext(source_file)[0]}.ris")
            
            with open(ris_filename, 'w', encoding='utf-8') as f:
                for idx, row in source_df.iterrows():
                    f.write(format_ris_record(row, idx + 1))
            
            print(f"Created RIS file: {ris_filename} ({len(source_df)} records)")

def format_ris_record(row: pd.Series, record_id: int) -> str:
    """
    Format a single record as RIS format.
    
    Args:
        row: Pandas Series containing record data
        record_id: Unique identifier for the record
    
    Returns:
        Formatted RIS record string
    """
    ris_record = []
    
    # Type of reference (assuming journal article/preprint)
    ris_record.append("TY  - JOUR")
    
    # Title
    if row.get('title'):
        ris_record.append(f"TI  - {row['title']}")
    
    # Authors
    if row.get('author'):
        author_string = str(row['author'])
    
        # Remove ellipsis and any leading/trailing punctuation/spaces
        author_string = re.sub(r'\.\.\.[,\s]*', '', author_string)
    
        # Split after "., " (period followed by comma and space)
        authors = re.split(r'\.,\s+', author_string)
    
        for i, author in enumerate(authors):
            author = author.strip()
            if author:
                # Add back the period to all authors except the last one
                if not author.endswith('.'):
                    author += '.'
                ris_record.append(f"AU  - {author}")

    # Publication year
    if row.get('year'):
        # Extract year from string (in case it contains extra text)
        year_match = re.search(r'\d{4}', str(row['year']))
        if year_match:
            ris_record.append(f"PY  - {year_match.group()}")
    
    # Abstract
    if row.get('abstract'):
        ris_record.append(f"AB  - {row['abstract']}")
    
    # URL/PDF link
    if row.get('pdf_link'):
        ris_record.append(f"UR  - {row['pdf_link']}")
    
    # Source file as note
    if row.get('source_file'):
        ris_record.append(f"N1  - Source: {row['source_file']}")
    
    # ID
    ris_record.append(f"ID  - {record_id}")
    
    # End of record
    ris_record.append("ER  - ")
    ris_record.append("")  # Empty line between records
    
    return '\n'.join(ris_record)

# Example usage
if __name__ == "__main__":
    # Define your file paths
    file_paths = [
        'data/preprints_scopus/page_1.html',
        'data/preprints_scopus/page_2.html',
        'data/preprints_scopus/page_3.html'
    ]
    
    # Process files and get combined DataFrame
    combined_data = process_scopus_files(file_paths, output_dir='data/ris_files')
    
    # Optionally save the combined DataFrame as CSV
    if not combined_data.empty:
        combined_data.to_csv('data/ris_files/combined_data.csv', index=False)
        print(f"Saved combined data to CSV: data/ris_files/combined_data.csv")
        
        # Display summary statistics
        print(f"\nSummary:")
        print(f"- Total records: {len(combined_data)}")
        print(f"- Records with titles: {len(combined_data[combined_data['title'] != ''])}")
        print(f"- Records with authors: {len(combined_data[combined_data['author'] != ''])}")
        print(f"- Records with abstracts: {len(combined_data[combined_data['abstract'] != ''])}")
        print(f"- Records with PDF links: {len(combined_data[combined_data['pdf_link'] != ''])}")