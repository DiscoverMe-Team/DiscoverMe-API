# this will enable to populate the scores from the PHQ-9 , GAD-7, and PSS

# utils.py

from collections import Counter

# Scoring Functions
def calculate_phq9_score(responses):
    """Calculate the total score for PHQ-9 based on responses."""
    return sum(responses)  # Sum of responses, assuming responses follow PHQ-9 scoring

def calculate_gad7_score(responses):
    """Calculate the total score for GAD-7 based on responses."""
    return sum(responses)

def calculate_perceived_stress_score(responses):
    """Calculate the total score for Perceived Stress Scale, with specific questions reversed."""
    # Reverse scores for specific questions (4, 5, 7, 8)
    reversed_responses = [(4 - resp) if i in [3, 4, 6, 7] else resp for i, resp in enumerate(responses)]
    return sum(reversed_responses)

# Interpretation Functions
def interpret_phq9_score(score):
    """Interpret PHQ-9 score for depression severity."""
    if score <= 4:
        return "Minimal depression"
    elif score <= 9:
        return "Mild depression"
    elif score <= 14:
        return "Moderate depression"
    elif score <= 19:
        return "Moderately severe depression"
    else:
        return "Severe depression"

def interpret_gad7_score(score):
    """Interpret GAD-7 score for anxiety severity."""
    if score <= 4:
        return "Minimal anxiety"
    elif score <= 9:
        return "Mild anxiety"
    elif score <= 14:
        return "Moderate anxiety"
    else:
        return "Severe anxiety"

def interpret_pss_score(score):
    """Interpret Perceived Stress Scale score for stress level."""
    if score <= 13:
        return "Low stress"
    elif score <= 26:
        return "Moderate stress"
    else:
        return "High stress"

# Validation Functions
def validate_responses(responses, max_value=3):
    """
    Validates that each response is within the expected range.
    Args:
        responses (list): List of responses to validate.
        max_value (int): The maximum allowable value for each response (default is 3).
    Returns:
        bool: True if all responses are valid, False otherwise.
    """
    return all(0 <= resp <= max_value for resp in responses)

# Mood Trend Analysis
def calculate_mood_trend(mood_logs):
    """
    Calculates the frequency of each mood over a given period.
    Args:
        mood_logs (list): List of mood log entries.
    Returns:
        dict: A dictionary with moods as keys and their frequency as values.
    """
    moods = [log.mood for log in mood_logs]
    return dict(Counter(moods))

# General Utility for Scoring and Interpretation
def score_and_interpret(assessment, responses):
    """
    Calculates and interprets the score for a given assessment type.
    Args:
        assessment (str): Type of assessment ('PHQ9', 'GAD7', 'PSS').
        responses (list): List of responses to score and interpret.
    Returns:
        tuple: A tuple with the calculated score and its interpretation.
    """
    if assessment == "PHQ9":
        score = calculate_phq9_score(responses)
        interpretation = interpret_phq9_score(score)
    elif assessment == "GAD7":
        score = calculate_gad7_score(responses)
        interpretation = interpret_gad7_score(score)
    elif assessment == "PSS":
        score = calculate_perceived_stress_score(responses)
        interpretation = interpret_pss_score(score)
    else:
        raise ValueError("Unknown assessment type")
    return score, interpretation

