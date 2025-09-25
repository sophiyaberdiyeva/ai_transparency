from instance.config import api_key
from llm_systematic_review.helpers import *
from llm_systematic_review.prompt_config import *
import io
import pandas as pd
import time

articles = pd.read_csv("data/sofiyas_title_abstract_scr.csv")
articles['Published Year']=articles['Published Year'].astype(str)
articles = articles[['Title', 'Abstract', 'Published Year', 'Covidence #']]
articles = articles.tail(277) #let's do the first half, then the second one

 
# API configuration (except for api_key)
base_url = "https://chat-ai.academiccloud.de/v1"
model = "llama-3.3-70b-instruct"

results = []

start = time.time()

for _, article in articles.iterrows():
    title, abstract, year, covidence_number = article.tolist()

    prompt_template = PromptTemplates.PROMPT_TITLE_ABSTRACT
    prompt_string = create_llm_abs_title_prompt_string(prompt_template, title, abstract, year, covidence_number)
    llm_response = get_llm_screening_decision(prompt_string, api_key, base_url, model)
    time.sleep(1)

    results.append(llm_response)
    
end = time.time()

end-start

final_df = pd.json_normalize(results)

final_df.to_csv("data/llm_title_abstract_third_part_2nd_try.csv", index=False)


first_part = pd.read_csv("data/llm_title_abstract_first_part_2nd_try.csv")
second_part = pd.read_csv("data/llm_title_abstract_second_part_2nd_try.csv")
third_part = pd.read_csv("data/llm_title_abstract_third_part_2nd_try.csv")

second_part = second_part.drop("error", axis = 1)
second_part = second_part.dropna(how = "all")

merged_raw = pd.concat([first_part, second_part, third_part])
merged_raw.to_csv("data/llm_title_abstract_second_version.csv", index=False)

articles = pd.read_csv("data/sofiyas_title_abstract_scr.csv")
joined_human_llm = articles.set_index('Covidence #').join(merged_raw.set_index('covidence_number'))

joined_human_llm['llm_final_decision_bin'] = joined_human_llm['final_decision'].map({'Include': 1, 'Exclude': 0})
joined_human_llm.to_csv('data/human_llm_title_abstract_second_version.csv')


to_screen_df = articles[~articles['Covidence #'].isin(merged_raw['covidence_number'])]

superfinal_df = pd.concat([merged_raw, third_part])
superfinal_df.to_csv("data/llm_title_abstract_first_version.csv", index=False)

joined_human_llm = articles.set_index('Covidence #').join(superfinal_df.set_index('covidence_number'))

joined_human_llm['llm_final_decision_bin'] = joined_human_llm['final_decision'].map({'Include': 1, 'Exclude': 0})
joined_human_llm.to_csv('data/human_llm_title_abstract_first_version.csv')
