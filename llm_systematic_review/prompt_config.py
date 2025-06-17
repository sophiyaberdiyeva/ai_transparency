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

    # --- INCLUSION CRITERIA PROMPTS ---

    PROMPT_HUMAN_PARTICIPANTS: Dict[str, Any] = {
  "role": "You are a meticulous research assistant screening articles for a systematic review.",
  "task": "Evaluate the following title and abstract to determine if the study involved human participants.",
  "criterion_to_check": "Inclusion Criterion 1 (Population): The study must involve human participants (e.g., subjects, users, a sample of people).",
  "instructions": [
    "Look for keywords such as 'participants', 'subjects', 'users', 'N = [number]', 'sample of', 'recruited', 'human experiment'.",
    "If the study appears to be purely theoretical, a simulation, a technical paper, or a literature review, it fails this criterion.",
    "Base your decision solely on the information in the provided text."
  ],
  "input_article": {
    "title": "",
    "abstract": ""
  },
  "output_format": {
    "description": "Provide your response as a JSON object with three keys: 'llm_decision_hp', 'llm_reasoning_hp', and 'llm_confidence_hp'.",
    "llm_decision_hp": "1 if the criterion is met (study includes humans), 0 if it is not.",
    "llm_reasoning_hp": "A brief, 1-2 sentence explanation for your decision, quoting from the abstract if possible.",
    "llm_confidence_hp": "A score from 1 (low confidence) to 5 (high confidence)."
  }
}
    """
    Template to check for Inclusion Criterion 1: Human Participants.
    
    This prompt asks the LLM to verify if a study involves human subjects,
    participants, or users. It is a fundamental check for empirical research
    involving people.
    
    Fill with the dictionary structure for this prompt.
    """

    PROMPT_PERSUASION_ATTEMPT: Dict[str, Any] = {
  "role": "You are a meticulous research assistant screening articles for a systematic review.",
  "task": "Evaluate the following title and abstract to determine if the study's intervention is a persuasion attempt.",
  "criterion_to_check": "Inclusion Criterion 2 (Intervention): The study must involve a persuasion attempt, defined as an intentional, goal-directed, message-based process aimed at shaping, reinforcing, or changing human attitudes, beliefs, or behaviors.",
  "instructions": [
    "Look for terms like 'persuade', 'convince', 'influence', 'change attitudes', 'shift beliefs', 'promote behavior', 'argumentation', 'debate'.",
    "Exclude studies where the AI interaction is the task completion without a goal to influence the participant's views or actions."
  ],
  "input_article": {
    "title": "",
    "abstract": ""
  },
  "output_format": {
    "description": "Provide your response as a JSON object with three keys: 'llm_decision_pa', 'llm_reasoning_pa', and 'llm_confidence_pa'.",
    "llm_decision_pa": "1 if the criterion is met (it is a persuasion attempt), 0 if it is not.",
    "llm_reasoning_pa": "A brief, 1-2 sentence explanation, specifying what kind of persuasion is being attempted.",
    "llm_confidence_pa": "A score from 1 (low confidence) to 5 (high confidence)."
  }
}
    """
    Template to check for Inclusion Criterion 2: Persuasion Attempt.

    This prompt directs the LLM to identify if the study's primary
    intervention or phenomenon of interest is an attempt to persuade,
    i.e., to influence attitudes, beliefs, or behaviors.
    
    Fill with the dictionary structure for this prompt.
    """

    PROMPT_LLM_AS_AGENT: Dict[str, Any] = {
  "role": "You are a meticulous research assistant screening articles for a systematic review.",
  "task": "Evaluate if the persuasion element is powered or delivered by an LLM or AI-driven generative text model.",
  "criterion_to_check": "Inclusion Criterion 3 (Technology): The persuasive agent must be an LLM, chatbot, conversational agent, or AI-driven generative text model.",
  "instructions": [
    "Look for keywords such as 'Large Language Model (LLM)', 'GPT', 'Llama', 'generative AI', 'chatbot', 'conversational agent'.",
    "Crucially, the LLM must be the *agent* of persuasion. Exclude studies where an LLM is used *only* for data analysis."
  ],
  "input_article": {
    "title": "",
    "abstract": ""
  },
  "output_format": {
    "description": "Provide your response as a JSON object with three keys:  'llm_decision_llm', 'llm_reasoning_llm', and 'llm_confidence_llm'.",
    "llm_decision_llm": "1 if the criterion is met (LLM is the agent), 0 if it is not.",
    "llm_reasoning_llm": "A brief, 1-2 sentence explanation clarifying the role of the LLM in the study.",
    "llm_confidence_llm": "A score from 1 (low confidence) to 5 (high confidence)."
  }
}
    
    """
    Template to check for Inclusion Criterion 3: LLM as Persuasion Agent.
    
    This prompt is designed to confirm that a Large Language Model (or a
    similar generative AI) is the active agent delivering the persuasive
    content, not merely a tool for background analysis or stimulus creation.
    
    Fill with the dictionary structure for this prompt.
    """

    PROMPT_EMPIRICAL_STUDY: Dict[str, Any] = {
  "role": "You are a meticulous research assistant screening articles for a systematic review.",
  "task": "Evaluate if the article is an empirical study reporting primary data.",
  "criterion_to_check": "Inclusion Criterion 4 (Study Type): The article must be an empirical study (e.g., experiment, quasi-experiment) reporting on primary data collection.",
  "instructions": [
    "Look for mentions of a methodology involving data collection, such as 'we conducted an experiment', 'we surveyed users'.",
    "Exclude articles that are explicitly 'review', 'meta-analysis', 'commentary', 'editorial', 'conceptual paper', or 'theoretical analysis'."
  ],
  "input_article": {
    "title": "",
    "abstract": ""
  },
  "output_format": {
    "description": "Provide your response as a JSON object with three keys: 'llm_decision_emp', 'llm_reasoning_emp', and 'llm_confidence_emp'.",
    "llm_decision_emp": "1 if the criterion is met (it is an empirical study), 0 if it is not.",
    "llm_reasoning_emp": "A brief explanation for your decision (e.g., 'The abstract describes a randomized controlled trial.').",
    "llm_confidence_emp": "A score from 1 (low confidence) to 5 (high confidence)."
  }
}
    
    """
    Template to check for Inclusion Criterion 4: Empirical Study Type.
    
    This prompt asks the LLM to determine if the article is an empirical
    study reporting primary data, and to exclude theoretical papers,
    reviews, commentaries, etc.
    
    Fill with the dictionary structure for this prompt.
    """

    # --- EXCLUSION CRITERIA PROMPTS ---
    
    PROMPT_EXCLUDE_MARKETING: Dict[str, Any] = {
  "role": "You are a meticulous research assistant screening articles for a systematic review.",
  "task": "Evaluate if the persuasion topic is unrelated to commercial marketing or consumer behavior.",
  "criterion_to_check": "Domain of Persuasion (Exclusion of Marketing): Studies where the primary goal is marketing, advertising, increasing sales, or influencing consumer purchasing behavior must be excluded.",
  "instructions": [
    "Exclude if the main persuasive goal is commercial. Look for keywords like 'marketing', 'advertising', 'e-commerce', 'brand perception', 'purchase intention', 'customer engagement'.",
    "Include if the domain is health, social issues, political beliefs, or reducing harmful beliefs.",
    "Your decision should be 1 if the topic is NOT marketing (passes the check), and 0 if the topic IS marketing (fails the check and should be excluded)."
  ],
  "input_article": {
    "title": "",
    "abstract": ""
  },
  "output_format": {
    "description": "Provide your response as a JSON object with three keys: 'llm_decision_mar', 'llm_reasoning_mar', and 'llm_confidence_mar'.",
    "llm_decision_mar": "1 if the study is NOT about marketing (Include). 0 if the study IS about marketing (Exclude).",
    "llm_reasoning_mar": "A brief explanation specifying the persuasion domain and why it is or is not commercial marketing.",
    "llm_confidence_mar": "A score from 1 (low confidence) to 5 (high confidence)."
  }
}
    
    """
    Template to check for an Exclusion Criterion: Domain of Persuasion.

    This prompt instructs the LLM to exclude studies where the primary
    persuasive goal is commercial, such as marketing, advertising, or
    influencing consumer purchasing decisions. A decision of '1' (Include)
    means the article is *not* about marketing and passes the check.
    
    Fill with the dictionary structure for this prompt.
    """

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