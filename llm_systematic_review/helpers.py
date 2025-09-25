from typing import Any, Dict
from openai import OpenAI
from openai.types.chat import ChatCompletionChunk 
import json

def create_llm_abs_title_prompt_string(prompt_template: Dict, title: str, abstract: str, year: str, covidence_number: str) -> str:
    """
    Fills a prompt template with article-specific information.

    Args:
        prompt_template: A dictionary representing the base prompt structure.
        title: The article's title.
        abstract: The article's abstract.

    Returns:
        A JSON-formatted string to be sent to the LLM.
    """
    # Deep copy the template to avoid modifying the original
    filled_prompt = json.loads(json.dumps(prompt_template))
    
    # Inject the specific article data into the prompt
    filled_prompt["input_article"]["title"] = title
    filled_prompt["input_article"]["abstract"] = abstract
    filled_prompt["input_article"]["year"] = year
    filled_prompt["input_article"]["covidence_number"] = covidence_number
    
    return json.dumps(filled_prompt, indent=2)

def create_llm_full_text_prompt_string(prompt_template: Dict, covidence_number: str, full_text: str) -> str:
    """
    Fills a prompt template with article-specific information.

    Args:
        prompt_template: A dictionary representing the base prompt structure.
        covidence_number: Unique number of article in Covidence
        full_text: Full text of article except for References section

    Returns:
        A JSON-formatted string to be sent to the LLM.
    """
    # Deep copy the template to avoid modifying the original
    filled_prompt = json.loads(json.dumps(prompt_template))
    
    # Inject the specific article data into the prompt
    filled_prompt["input_article"]["covidence_number"] = covidence_number
    filled_prompt["input_article"]["full_text"] = full_text
    
    return json.dumps(filled_prompt, indent=2)


def get_llm_screening_decision(prompt_string: str, api_key: str, base_url: str, model: str) -> Dict[str, Any]:
    """
    Sends a formatted prompt to the LLM API and returns the parsed JSON response.

    Args:
        prompt_string: The complete, JSON-formatted prompt string for the LLM.
        api_key: The API key for authentication.
        base_url: The base URL for the LLM API.
        model: The model to use for the LLM API request.

    Returns:
        A dictionary parsed from the LLM's JSON response.
        Returns an error dictionary if the response is not valid JSON.
    """
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # We ask the model to respond in JSON mode for more reliable output
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a meticulous research assistant. Your task is to evaluate a research article's abstract based on a specific criterion and respond ONLY with a valid JSON object matching the requested format."},
                {"role": "user", "content": prompt_string}
            ],
            model=model,
            response_format={"type": "json_object"}, # Use JSON mode for reliability
            seed = 42
        )
        
        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)

    except json.JSONDecodeError:
        return {
            "error": "Failed to decode JSON from LLM response.",
            "raw_response": response_content
        }
    except Exception as e:
        return {
            "error": f"An API call error occurred: {e}"
        }
    
