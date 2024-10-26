# this will enable to populate the scores from the PHQ-9 , GAD-7, and PSS

# In utils.py

def calculate_phq9_score(responses):
    return sum(responses)  # Sum of responses, assuming responses follow PHQ-9 scoring

def calculate_gad7_score(responses):
    return sum(responses)

def calculate_perceived_stress_score(responses):
    # Reverse scores for specific questions (4, 5, 7, 8)
    reversed_responses = [(4 - resp) if i in [3, 4, 6, 7] else resp for i, resp in enumerate(responses)]
    return sum(reversed_responses)
