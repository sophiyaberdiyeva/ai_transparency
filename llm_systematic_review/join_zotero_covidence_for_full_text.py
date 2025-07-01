import pandas as pd
from pathlib import Path

covidence_df = pd.read_csv("data/review_581959_screen_csv_20250603221248.csv") #data for full text screening

# Constructing dataframe with files from Zotero
zotero_df = pd.DataFrame(columns=["title", "authors", "year", "path"])

root_directory = "data/test_conversion/PDF"
root_path = Path(root_directory)

# Iterate through all subdirectories (numbered folders)
for folder_path in sorted(root_path.iterdir()):
    # Scan for txt files in the current folder
    for file_path in folder_path.iterdir():
        if file_path.suffix.lower() == '.txt':
            # Remove '_ocr' from the filename if present
            clean_name = file_path.name.replace('_ocr.txt', '')
            authors, year, title = clean_name.split(" - ")[:3]
            zotero_df = zotero_df.append({
                "title": title.strip(),
                "authors": authors.strip(),
                "year": year.strip(),
                "path": str(file_path)
            }, ignore_index=True)

max_title_length = max(zotero_df['title'].str.len())

covidence_df['cropped_title'] = covidence_df['Title'].str[:max_title_length]
# Merging the two dataframes on the cropped title
merged_df = pd.merge(covidence_df, zotero_df, left_on='cropped_title', right_on='title', how='left')

# Saving the merged dataframe to a CSV file
output_path = "data/merged_zotero_covidence_full_text.csv"
merged_df.to_csv(output_path, index=False)
