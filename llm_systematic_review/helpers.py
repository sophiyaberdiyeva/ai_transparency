from typing import List, Any
from openai import OpenAI

def split_into_batches(data: List[List[Any]]) -> List[List[List[Any]]]:
    """
    Splits the input dataset into batches of five rows each.

    Args:
        data: A list of rows, where each row is a list of values.

    Returns:
        A list of batches, where each batch contains up to five rows.
    """
    return [data[i:i + 5] for i in range(0, len(data), 5)]




def get_lmm_response(batch: list, api_key: str, base_url: str, model: str) -> dict:
    """
    Sends a batch of articles to the LMM API and returns the response.

    Args:
        batch: A list of articles, where each article is a dictionary with 'Title', 'Abstract', and 'Covidence #' keys.
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
    
    # Get stream
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content":
                    "You are given a list of articles, where each article is represented as a list containing the article title, abstract, and Covidence #, in that order. For each article in the provided list, generate a single line of comma-separated values (CSV format) with the following columns: Covidence #, involves human participants, involves persuasion, persuasion is LLM or AI-powered, is purely conceptual or theoretical article. For each criterion (involves human participants, involves persuasion, persuasion is LLM or AI-powered, is purely conceptual or theoretical article), use: '1' if the article meets the criterion, '0' if it does not, '-1' if you are unsure. Output one row per article and nothing else." + str(batch),
            }
        ],
        model=model,
        stream=True
    )
    
    # Print out the response
    # for chunk in stream:
    #     print(chunk.choices[0].delta.content or "", end="")
    
    return stream
