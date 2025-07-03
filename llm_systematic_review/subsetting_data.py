import pandas as pd

input_file = 'data/review_581959_screen_csv_20250703234512.csv' 
df = pd.read_csv(input_file)

subset_df = df.sample(n=50, random_state=1963)

output_file = 'data/subset_50_title_abstract_unscreened.csv'
subset_df.to_csv(output_file, index=False)

def create_ris_file(df, output_file):
    """
    Convert a DataFrame to RIS format and save to file.
    
    Parameters:
    df (pandas.DataFrame): DataFrame with bibliographic data
    output_file (str): Path to output RIS file
    """
    
    ris_content = []
    
    for index, row in df.iterrows():
        # Start each record
        ris_content.append("TY  - JOUR")  # Type: Journal article
        
        # Title
        if pd.notna(row['Title']):
            ris_content.append(f"TI  - {row['Title']}")
        
        # Authors - split by semicolon or comma and add each author
        if pd.notna(row['Authors']):
            authors = str(row['Authors']).split(';')
            for author in authors:
                author = author.strip()
                if author:
                    ris_content.append(f"AU  - {author}")
        
        # Abstract
        if pd.notna(row['Abstract']):
            ris_content.append(f"AB  - {row['Abstract']}")
        
        # Publication Year
        if pd.notna(row['Published Year']):
            ris_content.append(f"PY  - {int(row['Published Year'])}")
        
        # Publication Date (combine year and month)
        if pd.notna(row['Published Year']) and pd.notna(row['Published Month']):
            year = int(row['Published Year'])
            month = int(row['Published Month'])
            ris_content.append(f"DA  - {year}/{month:02d}")
        
        # Journal
        if pd.notna(row['Journal']):
            ris_content.append(f"JO  - {row['Journal']}")
            ris_content.append(f"T2  - {row['Journal']}")  # Secondary title (journal name)
        
        # Volume
        if pd.notna(row['Volume']):
            ris_content.append(f"VL  - {row['Volume']}")
        
        # Issue
        if pd.notna(row['Issue']):
            ris_content.append(f"IS  - {row['Issue']}")
        
        # Pages
        if pd.notna(row['Pages']):
            ris_content.append(f"SP  - {row['Pages']}")
        
        # DOI
        if pd.notna(row['DOI']):
            ris_content.append(f"DO  - {row['DOI']}")
        
        # Accession Number
        if pd.notna(row['Accession Number']):
            ris_content.append(f"AN  - {row['Accession Number']}")
        
        # Reference (URL or other reference)
        if pd.notna(row['Ref']):
            ris_content.append(f"UR  - {row['Ref']}")
        
        # Covidence # (preserved as custom field)
        if pd.notna(row['Covidence #']):
            ris_content.append(f"N1  - Covidence #: {row['Covidence #']}")
        
        # Study information
        if pd.notna(row['Study']):
            ris_content.append(f"N1  - Study: {row['Study']}")
        
        # Notes
        if pd.notna(row['Notes']):
            ris_content.append(f"N1  - Notes: {row['Notes']}")
        
        # Tags
        if pd.notna(row['Tags']):
            ris_content.append(f"KW  - {row['Tags']}")
        
        # End record
        ris_content.append("ER  - ")
        ris_content.append("")  # Empty line between records
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ris_content))
    
    print(f"RIS file created: {output_file}")
    print(f"Number of records: {len(df)}")

# Create RIS file from the subset
ris_output_file = 'data/subset_50_title_abstract_unscreened.ris'
create_ris_file(subset_df, ris_output_file)