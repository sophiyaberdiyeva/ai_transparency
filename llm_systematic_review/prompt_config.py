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
        "Strictly follow the specified output format and structure. Interpret the criteria description literally. If an abstract is not provided, the paper should be excluded."
    ),
    "inclusion_criteria": [
        {
            "name": "IC1: Participants",
            "description": "The study must involve human participants and report on data collected from them. Do not consider simple content creation like writing posts, comments, or essays as a form of participation."
        },
        {
            "name": "IC2: Intervention",
            "description": "The study must investigate a deliberate attempt to persuade (i.e., shape, reinforce, or change attitudes, beliefs, or behaviors) using messages. Exclude studies focused purely on task completion without persuasive intent. Exclude studies on education unless they are directly aimed at persuading people on societal topics (e.g., health, politics, misinformation, etc.)."
        },
        {
            "name": "IC3: Technology",
            "description": "It must be explicitly stated that the persuasive messages are delivered by an LLM or an LLM-based conversational agent (e.g., chatbot, assistant). Exclude studies where the LLM is only used for data analysis."
        },
        {
            "name": "IC4: Study Type",
            "description": "The article must be an empirical study (e.g., experiment, observational study) reporting on primary data. Exclude reviews, meta-analyses, commentaries, editorials, theoretical/conceptual papers, and study proposals for which no data has been collected."
        }
    ],
    "exclusion_criteria": [
        {
            "name": "EC1: Commercial Domain",
            "description": "The study must be excluded if its primary persuasive goal is commercial (e.g., marketing, advertising, increasing sales, customer service)."
        }
    ],
    "input_article": {
        "title": "",
        "abstract": "",
        "year": "",
        "covidence_number": ""
    },
    "output_format": {
        "covidence_number": "...",
        "inclusion_criteria_evaluation": {
            "llm_ic_1_participants": {
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
        "Strictly follow the specified output format and structure. Interpret the criteria description literally."
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
            "description": "It must be explicitly stated that the persuasive messages are delivered by an LLM or an LLM-based conversational agent (e.g., chatbot, assistant). Exclude studies where the LLM is only used for data analysis."
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
    
    PROMPT_EXTRACTION_PT_1: Dict[str, Any] ={
    "role": "You are an expert data extractor tasked with processing scientific articles for a systematic review.",
    "task_definition": "Given the full text of a scientific article and its Covidence number, extract specific data points and format them as a single line of comma-separated values (CSV) according to the specified column definitions and order. Ensure concise and accurate extraction. If information is missing for a specific field, use 'Not Reported' as instructed in the item's description.",
    "data_extraction_items": [
        {
            "column_number": 1,
            "column_name": "Covidence #",
            "description": "Extract the unique Covidence identifier provided for the article."
        },
        {
            "column_number": 2,
            "column_name": "Study Objectives",
            "description": "State the study's objectives specifically as they relate to persuasion."
        },
        {
            "column_number": 3,
            "column_name": "Location",
            "description": "Extract the country or region where the study was conducted. Provide the most complete and specific geographic location mentioned. If no location is reported, write: 'Not Reported'."
        },
        {
            "column_number": 4,
            "column_name": "Sample Age",
            "description": "Report the age characteristics of the participant sample. Format as: 'Mean = [value], SD = [value], Range = [value-value]'. Omit any specific part (e.g., SD) if it is not reported. If no age information is provided at all, write: 'Not Reported'."
        },
        {
            "column_number": 5,
            "column_name": "Sample Gender Distribution",
            "description": "Report the gender distribution of the participant sample, providing the percentage or count for each gender reported (e.g., 'Female: 45%, Male: 52%, Non-binary/Other: 3%'). If not provided, write: 'Not Reported'."
        },
        {
            "column_number": 6,
            "column_name": "Sample Education Level",
            "description": "Describe the educational background of the participant sample as a distribution (e.g., 'High School: 20%, Some College: 35%, Bachelor's Degree: 40%'). If not provided, write: 'Not Reported'."
        },
        {
            "column_number": 7,
            "column_name": "Interactive",
            "description": "Indicate whether the persuasion was interactive. Use one of the following values: 'Yes' if participants engaged in communication with the AI agent, 'Partially' if some interaction occurred but was limited or unclear, 'No' if it was one-way exposure to AI content without participant interaction or 'Not Reported'."
        },
        {
            "column_number": 8,
            "column_name": "Interaction Description",
            "description": "If the 'Interactive' status is 'Yes' or 'Partially', briefly describe how the participant interacted with the AI agent. If 'No', write: 'Non-interactive'."
        },
        {
            "column_number": 9,
            "column_name": "Domain",
            "description": "Identify the topic or application domain of the persuasion (e.g., health, politics, social issues). If it's another category, specify it."
        },
        {
            "column_number": 10,
            "column_name": "Informed Participants",
            "description": "Indicate if participants were informed about the AI. Use one of the following: 'Yes, explicitly', 'Yes, implicitly', 'No', or 'Not Reported'."
        },
        {
            "column_number": 11,
            "column_name": "Disclosure Delivery",
            "description": "Provide the exact verbatim wording of the AI disclosure. If no disclosure is provided, write: 'Not Reported'."
        }
    ],
    "input_format": {
        "covidence_number": "...",
        "full_text": "..."
    },
    "output_format": {
        "type": "CSV",
        "description": "A single line containing exactly 11 comma-separated values, with each value corresponding to the data extraction items in the specified order."
    }
}
    
    PROMPT_EXTRACTION_PT_2: Dict[str, Any] ={
    "role": "You are an expert data extractor tasked with processing scientific articles for a systematic review.",
    "task_definition": "Given the full text of a scientific article and its Covidence number, extract specific data points related to experimental prompts and instructions. The output must be a single line of comma-separated values (CSV) in the exact order specified. Be concise and accurate, using 'Not Reported' where information is not found.",
    "data_extraction_items": [
        {
            "column_number": 1,
            "column_name": "Covidence number",
            "description": "Extract the unique Covidence identifier provided for the article."
        },
        {
            "column_number": 2,
            "column_name": "Prompt Availability",
            "description": "Indicate if the LLM prompt(s) are available. Use one of the following values: 'Yes' if prompt(s) are fully available, 'Partially' if some, but not all, prompts or prompt content are provided, 'No' if prompt(s) are explicitly not shared, or 'Not Reported'."
        },
        {
            "column_number": 3,
            "column_name": "Prompt Extract/Summary",
            "description": "Provide a direct extract or a concise summary of the LLM prompt(s). If unavailable, write: 'Not Reported'."
        },
        {
            "column_number": 4,
            "column_name": "Prompt Location",
            "description": "Indicate where the prompt is located. Use one of the following values: 'Main text', 'Supplement', 'Appendix', 'External repository', 'Available on request', or 'Not available'."
        },
        {
            "column_number": 5,
            "column_name": "Persuasive Prompt Content",
            "description": "Specify if the prompt explicitly includes a persuasive goal or persuasive strategy. Use one of the following values: 'Yes', 'No', 'Unclear' if prompt is ambiguous or indirect, or 'Not Applicable'."
        },
        {
            "column_number": 6,
            "column_name": "Discouragement of Disclosure",
            "description": "Indicate if the prompt discourages AI agent revealing the persuasion goal or persuasive strategy to the interaction partner. Use one of the following values: 'Yes', 'No', 'Unclear', or 'Not Applicable'."
        },
        {
            "column_number": 7,
            "column_name": "Participant Instruction Availability",
            "description": "Indicate if participant instructions are available. Use one of the following values: 'Yes', 'Partially' if some instructions are provided but not in full, or 'No'."
        },
        {
            "column_number": 8,
            "column_name": "Participant Instruction Extract/Summary",
            "description": "Provide a direct extract or a concise summary of the participant instructions. If not available, write: 'Not Reported'."
        },
        {
            "column_number": 9,
            "column_name": "Persuasive Nature in Instructions",
            "description": "Determine if instructions reveal persuasive intent. Use one of the following values: 'Yes, explicitly' if instructions clearly state persuasive intent, 'Yes, implicitly' if persuasive intent is implied or indirectly conveyed, 'No' if instructions do not indicate persuasive intent, or 'Not Reported' if no relevant information is available."
        }
    ],
    "input_format": {
        "covidence_number": "...",
        "full_text": "..."
    },
    "output_format": {
        "type": "CSV",
        "description": "A single line containing exactly 9 comma-separated values, corresponding to the data extraction items in the specified order."
    }
}
    
    PROMPT_EXTRACTION_PT_3: Dict[str, Any] ={
    "role": "You are an expert data extractor tasked with processing scientific articles for a systematic review.",
    "task_definition": "Given the full text of a scientific article and its Covidence number, extract specific data points related to debriefing, methodology, and ethical considerations. The output must be a single line of comma-separated values (CSV) in the exact order specified. Be concise and accurate, using 'Not Reported' where information is missing or not stated in the article.",
    "data_extraction_items": [
        {
            "column_number": 1,
            "column_name": "Covidence number",
            "description": "Extract the unique Covidence identifier provided for the article."
        },
        {
            "column_number": 2,
            "column_name": "Debriefing Reported",
            "description": "Indicate if a debriefing procedure was mentioned. Use one of the following values: 'Yes' or 'No'."
        },
        {
            "column_number": 3,
            "column_name": "Debriefing Discloses AI",
            "description": "If debriefing was reported, indicate if it disclosed AI involvement. Use one of the following values: 'Yes', 'No', 'Unclear' or 'Not Applicable' (if no debriefing was reported)."
        },
        {
            "column_number": 4,
            "column_name": "Debriefing Discloses Persuasion",
            "description": "If debriefing was reported, indicate if it disclosed persuasive intent. Use one of the following values: 'Yes', 'No', 'Unclear' or 'Not Applicable' (if no debriefing was reported)."
        },
        {
            "column_number": 5,
            "column_name": "Debriefing Extract",
            "description": "Provide a verbatim extract or concise summary of the debriefing content. If debriefing is not reported, write: 'Not Reported'."
        },
        {
            "column_number": 6,
            "column_name": "AI System Used",
            "description": "Specify the name of the LLM or AI system used (e.g., GPT-3.5, Claude 2). If not mentioned, write: 'Not Reported'."
        },
        {
            "column_number": 7,
            "column_name": "Study Design Type",
            "description": "Identify the study design (e.g., RCT, quasi-experiment, observational, etc.)."
        },
        {
            "column_number": 8,
            "column_name": "Study Setting",
            "description": "Specify the study setting. Use one of the following values: 'Lab study', 'Online study', 'Field study', 'Other (specify): ...', or 'Not Reported'."
        },
        {
            "column_number": 9,
            "column_name": "Ethical Approval Reported",
            "description": "Indicate whether ethical approval was reported. Use one of the following values: 'Yes' or 'No'."
        }
    ],
    "input_format": {
        "covidence_number": "...",
        "full_text": "..."
    },
    "output_format": {
        "type": "CSV",
        "description": "A single line containing exactly 9 comma-separated values, corresponding to the data extraction items in the specified order."
    }
}