from instance.config import api_key
from llm_systematic_review.helpers import *
from llm_systematic_review.prompt_config import *
import io
import pandas as pd
import time
import os
import re
from pathlib import Path

articles = pd.read_csv("data/merged_zotero_covidence_full_text.csv")
articles = articles.head(1)

 
# API configuration (except for api_key)
base_url = "https://chat-ai.academiccloud.de/v1"
model = "llama-3.3-70b-instruct"

results = []

for idx, row in articles.iterrows():
    covidence_number = row['Covidence #']
    path = row['path']
    with open(path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    prompt_template = PromptTemplates.PROMPT_FULL_TEXT
    prompt_string = create_llm_full_text_prompt_string(prompt_template, covidence_number, full_text)
    llm_response = get_llm_screening_decision(prompt_string, api_key, base_url, model)
    time.sleep(1)

    results.append(llm_response)

final_df = pd.json_normalize(results)

final_df.to_csv("data/llm_full_text_50.csv", index=False)
