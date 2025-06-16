from instance.config import api_key
from llm_systematic_review.helpers import *
import io
import pandas as pd
import time

articles = pd.read_csv("data/review_581959_screen_csv_20250603221248.csv")
articles = articles[['Title', 'Abstract', 'Covidence #']]
articles = articles.head(50)

 
# API configuration (except for api_key)
base_url = "https://chat-ai.academiccloud.de/v1"
model = "llama-3.3-70b-instruct"

results = []

start_time = time.time()
# Iterate through articles, get LLM decisions as csv and store them in Dataframe
for _, article in articles.iterrows():
    response = llm_title_abstract(article.tolist(), api_key, base_url, model)

    content = response.choices[0].message.content

    if content.strip():
        response_df = pd.read_csv(io.StringIO(content), header=None)
        results.append(response_df)
        
    time.sleep(2)

end_time = time.time()

print('Execution time:', end_time-start_time)
final_df = pd.concat(results, ignore_index=True)
final_df.columns = ['llm_covidence_no', 'llm_human_participants', 'llm_involves_persuasion', 'llm_persuasion_is_ai', 'llm_is_marketing']
final_df['llm_final_decision'] = final_df.apply(lambda x: 1 if x.llm_human_participants == 1 and x.llm_involves_persuasion == 1 and x.llm_persuasion_is_ai == 1 and x.llm_is_marketing == 0 else 0, axis=1)

final_df.to_csv("data/llm_title_abstract_50.csv", index=False)
