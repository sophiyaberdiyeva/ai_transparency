from typing import Dict, Any

class PromptTemplates:
    """
    A container class for storing LLM prompt templates for the systematic review.

    This class centralizes all prompt structures used for screening articles.
    Each class attribute represents a specific screening step and holds a 
    dictionary that serves as the template for the prompt. The class is not
    intended to be instantiated; it should be used as a namespace to access 
    the templates, e.g., `PromptTemplates.PROMPT_TITLE_ABSTRACT`.
    """

    PROMPT_TITLE_ABSTRACT: Dict[str, Any] = {
    "role": "You are an expert academic reviewer screening research papers for a systematic review on LLM-driven persuasion. Your task is to determine if a paper should be included based on its title and abstract.",
    "task_definition": (
        "Evaluate the provided article against each inclusion and exclusion criterion. "
        "For each criterion, provide brief reasoning and a 'Yes/No' decision. "
        "Conclude with a final 'Include' or 'Exclude' decision. "
        "Strictly follow the specified output format and structure."
    ),
    "inclusion_criteria": [
        {
            "name": "IC1: Population",
            "description": "The study must involve human participants and report on data collected from them."
        },
        {
            "name": "IC2: Intervention",
            "description": "The study must investigate a deliberate attempt to persuade (i.e., shape, reinforce, or change attitudes, beliefs, or behaviors) using messages. Exclude studies focused purely on task completion without persuasive intent."
        },
        {
            "name": "IC3: Technology",
            "description": "The persuasive messages must be delivered by an LLM, chatbot, conversational agent, or similar generative AI. Exclude studies where the LLM is only used for data analysis."
        },
        {
            "name": "IC4: Study Type",
            "description": "The article must be an empirical study (e.g., experiment, observational study) reporting on primary data. Exclude reviews, meta-analyses, commentaries, editorials, and theoretical/conceptual papers."
        }
    ],
    "exclusion_criteria": [
        {
            "name": "EC1: Commercial Domain",
            "description": "The study must be excluded if its primary persuasive goal is commercial (e.g., marketing, advertising, increasing sales)."
        }
    ],
    "input_article": {
        "title": "",
        "abstract": "",
        "covidence_number": ""
    },
    "output_format": {
        "covidence_number": "...",
        "inclusion_criteria_evaluation": {
            "llm_ic_1_population": {
                "reasoning": "...",
                "decision": "Yes/No"
            },
            "llm_ic_2_intervention": {
                "reasoning": "...",
                "decision": "Yes/No"
            },
            "llm_ic_3_technology": {
                "reasoning": "...",
                "decision": "Yes/No"
            },
            "llm_ic_4_study_type": {
                "reasoning": "...",
                "decision": "Yes/No"
            }
        },
        "exclusion_criteria_evaluation": {
            "llm_ec_1_domain": {
                "reasoning": "...",
                "decision": "Yes/No"
            }
        },
        "final_decision": "Include/Exclude"
    }
}

    PROMPT_FULL_TEXT: Dict[str, Any] = {
    "role": "You are an expert academic reviewer screening research papers for a systematic review on LLM-driven persuasion. Your task is to determine if a paper should be included based on its full text provided below.",
    "task_definition": (
        "Evaluate the provided article against each inclusion and exclusion criterion. "
        "For each criterion, provide brief reasoning and a 'Yes/No' decision. "
        "Conclude with a final 'Include' or 'Exclude' decision. "
        "Strictly follow the specified output format and structure."
    ),
    "inclusion_criteria": [
        {
            "name": "IC1: Population",
            "description": "The study must involve human participants and report on data collected from them."
        },
        {
            "name": "IC2: Intervention",
            "description": "The study must investigate a deliberate attempt to persuade (i.e., shape, reinforce, or change attitudes, beliefs, or behaviors) using messages. Exclude studies focused purely on task completion without persuasive intent."
        },
        {
            "name": "IC3: Technology",
            "description": "The persuasive messages must be delivered by an LLM, chatbot, conversational agent, or similar generative AI. Exclude studies where the LLM is only used for data analysis."
        },
        {
            "name": "IC4: Study Type",
            "description": "The article must be an empirical study (e.g., experiment, observational study) reporting on primary data. Exclude reviews, meta-analyses, commentaries, editorials, and theoretical/conceptual papers."
        }
    ],
    "exclusion_criteria": [
        {
            "name": "EC1: Commercial Domain",
            "description": "The study must be excluded if its primary persuasive goal is commercial (e.g., marketing, advertising, increasing sales)."
        }
    ],
    "input_article": {
        "covidence_number": "",
        "full_text": ""
    },
    "output_format": {
        "covidence_number": "...",
        "inclusion_criteria_evaluation": {
            "llm_ic_1_population": {
                "reasoning": "...",
                "decision": "Yes/No"
            },
            "llm_ic_2_intervention": {
                "reasoning": "...",
                "decision": "Yes/No"
            },
            "llm_ic_3_technology": {
                "reasoning": "...",
                "decision": "Yes/No"
            },
            "llm_ic_4_study_type": {
                "reasoning": "...",
                "decision": "Yes/No"
            }
        },
        "exclusion_criteria_evaluation": {
            "llm_ec_1_domain": {
                "reasoning": "...",
                "decision": "Yes/No"
            }
        },
        "final_decision": "Include/Exclude"
    }
    }
    
