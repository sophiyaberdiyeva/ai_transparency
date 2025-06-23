from typing import Dict, Any

class PromptTemplates:
    """
    A container class for storing LLM prompt templates for the systematic review.

    This class centralizes all prompt structures used for screening articles.
    Each class attribute represents a specific screening criterion and holds a 
    dictionary that serves as the template for the prompt. The class is not
    intended to be instantiated; it should be used as a namespace to access 
    the templates, e.g., `PromptTemplates.PROMPT_HUMAN_PARTICIPANTS`.
    """

    PROMPT_FULL_CRITERIA: Dict[str, Any] = {
        "role": "You are an expert academic reviewer specializing in the screening of research papers for systematic reviews. You are conducting a systematic review  that aims to comprehensively document and analyze current transparency practices in empirical studies that utilize LLMs for persuasion. Your task is to determine if a study should be included based on its title and abstract.",
        "task_definition": (
            "Your primary task is to assess whether a given article, based on its title and abstract, meets the predefined criteria. "
            "You must evaluate the article against each inclusion and exclusion criterion, provide a brief reasoning for your decision on each, and then make a final decision ('Include' or 'Exclude'). Stricly follow the provided output format, order and structure."
        ),
        "inclusion_criteria": [
            {
                "name": "Inclusion Criterion 1 (Population)",
                "description": (
                    "The study must involve human participants (e.g., subjects, users, a sample of people). "
                    "If the study appears to be purely theoretical, a simulation, a technical paper, or a literature review, it fails this criterion. "
                    "Base your decision solely on the information in the provided text. The research must report on data collected from human beings."
                )
            },
            {
                "name": "Inclusion Criterion 2 (Intervention)",
                "description": (
                    "The study must involve a persuasion attempt, defined as an intentional, goal-directed, message-based process aimed at shaping, reinforcing, or changing human attitudes, beliefs, or behaviors. "
                    "This means the study investigates an effort to influence what people think or do. "
                    "Exclude studies where the AI interaction is focused on task completion without an underlying goal to influence the participant's views or actions."
                )
            },
            {
                "name": "Inclusion Criterion 3 (Technology)",
                "description": (
                    "The persuasive agent must be an LLM, chatbot, conversational agent, or AI-driven generative model. "
                    "The core of the intervention must be that a Large Language Model or a similar generative AI is the one delivering the persuasive message. "
                    "Exclude studies where an LLM is used only for analyzing data rather than acting as the persuader."
                )
            },
            {
                "name": "Inclusion Criterion 4 (Study Type)",
                "description": (
                    "The article must be an empirical study (e.g., experiment, quasi-experiment, observational study) reporting on primary data collection. "
                    "This means the authors must have conducted their own study and are reporting their own results, not just discussing others' work. "
                    "Exclude articles that are explicitly a 'review', 'meta-analysis', 'commentary', 'editorial', 'conceptual paper', or 'theoretical analysis'."
                )
            }
        ],
        "exclusion_criteria": [
            {
                "name": "Exclusion Criterion 1 (Domain of Persuasion)",
                "description": (
                    "Studies where the primary goal is marketing, advertising, increasing sales, or influencing consumer purchasing behavior must be excluded. "
                    "Exclude if the main persuasive goal is commercial."
                )
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


# --- Example of how to use the class after filling it ---
#
# from prompt_config import PromptTemplates
#
# # Access a specific template
# template = PromptTemplates.PROMPT_HUMAN_PARTICIPANTS
#
# # You can then pass this template to your functions
# final_prompt_str = create_llm_prompt_string(
#     prompt_template=template,
#     title="Some Article Title",
#     abstract="Some article abstract..."
# )