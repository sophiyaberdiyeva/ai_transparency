from instance.config import api_key
from llm_systematic_review.helpers import *
import io
import pandas as pd

articles = pd.read_csv("data/review_581959_screen_csv_20250603221248.csv")
articles = articles[['Title', 'Abstract', 'Covidence #']]
article_batches = split_into_batches(articles, batch_size = 5)
article_batches

# API configuration (except for api_key)
base_url = "https://chat-ai.academiccloud.de/v1"
model = "llama-3.3-70b-instruct" # Choose any available model

results = []

# Iterate through batches, get LLM decisions as csv and store them in Dataframe
for batch in article_batches:
    response = get_lmm_response(batch, api_key, base_url, model)
    
    csv_text = ""

    for chunk in response:
        if 'choices' in chunk and chunk['choices']:
            content = chunk['choices'][0].get('delta', {}).get('content', '')
            if content:
                csv_text += content

    if csv_text.strip():
        batch_df = pd.read_csv(io.StringIO(csv_text), header=None)
        results.append(batch_df)

llm_decisions = pd.concat(results, ignore_index=True)
llm_decisions.columns = ['covidence_no', 'human_participants', 'involves_persuasion', 'persuasion_is_ai', 'is_theoretical']
llm_decisions.to_csv("data/llm_decisions.csv", index=False)
