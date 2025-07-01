from instance.config import api_key
from llm_systematic_review.helpers import *
from llm_systematic_review.prompt_config import *
import io
import pandas as pd
import time
import os
import re
from pathlib import Path

articles = pd.read_csv("data/review_581959_screen_csv_20250603221248.csv")
articles = articles[['Title', 'Covidence #']]
articles = articles.head(1)

 
# API configuration (except for api_key)
base_url = "https://chat-ai.academiccloud.de/v1"
model = "llama-3.3-70b-instruct"

results = []

root_directory = "data/test_conversion/PDF"
root_path = Path(root_directory)

# Iterate through all subdirectories
for folder_path in root_path.iterdir():
    # Look for OCR text file in this folder
    ocr_file = list(folder_path.glob("*_ocr.txt"))[0]
    
    
    




for _, article in articles.iterrows():
    covidence_number = article.tolist()

    prompt_template = PromptTemplates.PROMPT_FULL_TEXT
    prompt_string = create_llm_full_text_prompt_string(prompt_template, covidence_number, full_text)
    llm_response = get_llm_screening_decision(prompt_string, api_key, base_url, model)
    time.sleep(1)

    results.append(llm_response)

final_df = pd.json_normalize(results)

final_df.to_csv("data/llm_title_abstract_50.csv", index=False)
