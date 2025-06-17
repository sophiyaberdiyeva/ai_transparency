from instance.config import api_key
from llm_systematic_review.helpers import *
from llm_systematic_review.prompt_config import *
import io
import pandas as pd
import time

articles = pd.read_csv("data/review_581959_screen_csv_20250603221248.csv")
articles = articles[['Title', 'Abstract', 'Covidence #']]
articles = articles.head(1)

 
# API configuration (except for api_key)
base_url = "https://chat-ai.academiccloud.de/v1"
model = "llama-3.3-70b-instruct"

results = {}

start_time = time.time()
# Iterate through titles, abstracts and covidence numbers, get LLM decisions as dictionaries and store them in Dataframe
for _, article in articles.iterrows():
    title, abstract, covidence_no = article.tolist()
    article_dict = {}
    
    for prompt_template_name in dir(PromptTemplates):
        if prompt_template_name.startswith("PROMPT_"):
            prompt_template = getattr(PromptTemplates, prompt_template_name)
            prompt_string = create_llm_prompt_string(prompt_template, title, abstract)
            llm_response = get_llm_screening_decision(prompt_string, api_key, base_url, model)
            article_dict.update(llm_response)
            time.sleep(1)
        
    results.update({covidence_no: article_dict})

end_time = time.time()

print('Execution time:', end_time-start_time)

final_df = pd.DataFrame.from_dict(results, orient='index')
final_df['llm_final_decision'] = (final_df[[col for col in final_df.columns if col.startswith('decision_')]] == 1).all(axis=1).astype(int)

final_df.to_csv("data/llm_title_abstract_50.csv", index=False)
