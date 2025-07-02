from instance.config import api_key
from llm_systematic_review.helpers import *
from llm_systematic_review.prompt_config import *
import io
import pandas as pd
import time
import os
import re
from pathlib import Path

extr_covidence_df = pd.read_csv("data/review_581959_included_csv_20250628001529.csv") #articles exported from covidence - those left after full text screening
full_text_df = pd.read_csv("data/merged_zotero_covidence_full_text.csv") #old full file with articles with paths for full text screening

# Filtering the full_text_df to only include articles that are in extr_covidence_df
filtered_df = full_text_df[full_text_df['Covidence #'].isin(extr_covidence_df['Covidence #'])]

# Saving the filtered dataframe to a CSV file
filtered_df.to_csv("data/merged_zotero_covidence_data_extraction.csv", index=False)
filtered_df = filtered_df.head(1)

# API configuration (except for api_key)
base_url = "https://chat-ai.academiccloud.de/v1"
model = "llama-3.3-70b-instruct"

# Loop number 1

results_1 = []

for idx, row in filtered_df.iterrows():
    covidence_number = row['Covidence #']
    path = row['path']
    with open(path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    prompt_template = PromptTemplates.PROMPT_EXTRACTION_PT_1
    prompt_string = create_llm_full_text_prompt_string(prompt_template, covidence_number, full_text)
    llm_response = get_llm_screening_decision(prompt_string, api_key, base_url, model)
    results_1.append(llm_response.strip())
    time.sleep(1)

# Prepare DataFrame from CSV
columns_pt_1 = [
    "covidence_number",
    "study_objectives",
    "location",
    "sample_age",
    "sample_gender_distribution",
    "sample_education_level",
    "interactive",
    "interaction_description",
    "domain",
    "informed_participants",
    "disclosure_delivery"
]

with open('llm_data_extraction_pt_1.csv', 'w', encoding='utf-8') as f:
    f.write(",".join(columns) + '\n')
    for line in results_1:
        f.write(line + '\n')

# Convert results (list of CSV lines) to DataFrame
pt_1_df = pd.read_csv('llm_data_extraction_pt_1.csv', dtype={'covidence_number': str})

# Loop number 2

results_2 = []

for idx, row in articles.iterrows():
    covidence_number = row['Covidence #']
    path = row['path']
    with open(path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    prompt_template = PromptTemplates.PROMPT_EXTRACTION_PT_2
    prompt_string = create_llm_full_text_prompt_string(prompt_template, covidence_number, full_text)
    llm_response = get_llm_screening_decision(prompt_string, api_key, base_url, model)
    results_2.append(llm_response.strip())
    time.sleep(2)

# Prepare DataFrame from CSV
columns_pt_2 = [
    "covidence_number",
    "prompt_availability",
    "prompt_extract",
    "prompt_location",
    "pers_prompt_content",
    "discouragement_of_disclosure",
    "participant_instr_avail",
    "participant_instr",
    "pers_nature_in_instr"
]

with open('llm_data_extraction_pt_2.csv', 'w', encoding='utf-8') as f:
    f.write(",".join(columns_pt_2) + '\n')
    for line in results_2:
        f.write(line + '\n')

# Convert results (list of CSV lines) to DataFrame
pt_2_df = pd.read_csv('llm_data_extraction_pt_2.csv', dtype={'covidence_number': str})

# Loop number 3

results_3 = []

for idx, row in articles.iterrows():
    covidence_number = row['Covidence #']
    path = row['path']
    with open(path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    prompt_template = PromptTemplates.PROMPT_EXTRACTION_PT_3
    prompt_string = create_llm_full_text_prompt_string(prompt_template, covidence_number, full_text)
    llm_response = get_llm_screening_decision(prompt_string, api_key, base_url, model)
    results_3.append(llm_response.strip())
    time.sleep(3)

# Prepare DataFrame from CSV
columns_pt_3 = [
    "covidence_number",
    "debriefing_reported",
    "debriefing_discloses_ai",
    "debriefing_discloses_pers",
    "debriefing_extract",
    "ai_system_used",
    "study_design_type",
    "study_setting",
    "ethical_approval_reported"
]

with open('llm_data_extraction_pt_3.csv', 'w', encoding='utf-8') as f:
    f.write(",".join(columns_pt_3) + '\n')
    for line in results_3:
        f.write(line + '\n')

# Convert results (list of CSV lines) to DataFrame
pt_3_df = pd.read_csv('llm_data_extraction_pt_3.csv', dtype={'covidence_number': str})


# Combine all DataFrames based on 'covidence_number'

merged_df = pt_1_df.merge(pt_2_df, on="covidence_number", how="outer", suffixes=('_pt1', '_pt2'))
merged_df = merged_df.merge(pt_3_df, on="covidence_number", how="outer", suffixes=('', '_pt3'))

# Join with the original filtered DataFrame to include paths and other metadata
merged_df = merged_df.merge(filtered_df, left_on='covidence_number', right_on='Covidence #', how='left')

# Save the merged DataFrame
merged_df.to_csv("data/llm_data_extraction_all.csv", index=False)
