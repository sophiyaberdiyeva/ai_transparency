from typing import List, Any
from openai import OpenAI
from typing import Generator
from openai.types.chat import ChatCompletionChunk 

def llm_title_abstract(article: list, api_key: str, base_url: str, model: str) -> Generator[ChatCompletionChunk, None, None]:
    """
    Sends a batch of articles to the LMM API and returns the response.

    Args:
        article: A list with 'Title', 'Abstract', and 'Covidence #' keys.
        api_key: The API key for authentication.
        base_url: The base URL for the LMM API.
        model: The model to use for the LMM API request.

    Returns:
        The response from the LMM API.
    """
        
    # Start OpenAI client
    client = OpenAI(
        api_key = api_key,
        base_url = base_url
    )
    
    prompt = "Input: A list containing [title, abstract, Covidence #]. Task: Determine the following for each article and output one CSV-formatted line with these columns: Covidence #, involves human participants in the sample (1/0/-1), involves persuasion as intervention (1/0/-1), persuasion is performed with LLM or AI usage in text generation (1/0/-1), persuasion relates to marketing or consumer behavior (1/0/-1). Persuasion is defined as an intentional, goal-directed, message-based process aimed at shaping, reinforcing, or changing human attitudes, beliefs, or behaviors. Use 1 if the criterion is clearly met, 0 if clearly not met, and -1 if uncertain based on the information provided. Return only the single CSV row. Do not include any explanation or extra text."+ str(article)
    
    # Get response
    chat_completion = client.chat.completions.create(
        messages=[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content": prompt}],
        model= model,
    )
  
    # Print out the response
    #for chunk in resp:
        #print(chunk.choices[0].delta.content or "", end="")
    
    return chat_completion
