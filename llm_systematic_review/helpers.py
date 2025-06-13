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
    
    prompt = "Input: A list with [title, abstract, Covidence #].\n Task: Output one CSV line: Covidence #, involves human participants (1/0/-1), involves persuasion (1/0/-1), persuasion is LLM/AI-powered (1/0/-1), purely conceptual/theoretical (1/0/-1), about marketing or customer behavior (1/0/-1). Use 1 if yes, 0 if no, -1 if unclear. Return only the CSV row without explanation. "+ str(article)
    
    # Get response
    chat_completion = client.chat.completions.create(
        messages=[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content": prompt}],
        model= model,
    )
  
    # Print out the response
    #for chunk in resp:
        #print(chunk.choices[0].delta.content or "", end="")
    
    return chat_completion
