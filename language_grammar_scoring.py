import re
from collections import Counter

def calculate_ttr(transcript: str) -> float:
    """
    Calculate Type-Token Ratio (TTR)
    TTR = Distinct words / Total words
    """
    words = re.findall(r'\b\w+\b', transcript.lower())
    
    if len(words) == 0:
        return 0
    
    distinct_words = len(set(words))
    total_words = len(words)
    
    ttr = distinct_words / total_words
    return ttr

def score_vocabulary_richness(transcript: str) -> dict:
    """
    Score vocabulary richness using TTR (0-10 points)
    0.9–1.0: 10 pts
    0.7–0.89: 8 pts
    0.5–0.69: 6 pts
    0.3–0.49: 4 pts
    0–0.29: 2 pts
    """
    ttr = calculate_ttr(transcript)
    
    if ttr >= 0.9:
        score = 10
        level = "Excellent"
    elif ttr >= 0.7:
        score = 8
        level = "Very Good"
    elif ttr >= 0.5:
        score = 6
        level = "Good"
    elif ttr >= 0.3:
        score = 4
        level = "Fair"
    else:
        score = 2
        level = "Poor"
    
    feedback = f"Vocabulary richness: {level} (TTR: {ttr:.3f})"
    
    return {
        'vocabulary': score,
        'total': score,
        'feedback': feedback,
        'metrics': {
            'ttr': ttr,
            'distinct_words': len(set(re.findall(r'\b\w+\b', transcript.lower()))),
            'total_words': len(re.findall(r'\b\w+\b', transcript.lower()))
        }
    }

def count_grammar_errors(transcript: str) -> int:
    """
    Simple grammar error detection using pattern matching
    Counts obvious errors to estimate quality, not to perfectly catch all errors
    Avoids overfitting to specific error patterns
    """
    errors = 0
    text_lower = transcript.lower()
    
    # Common grammar issues - but use conservative detection
    
    # Subject-verb agreement (only obvious cases)
    if re.search(r'\byou\s+is\b', text_lower):
        errors += 1
    if re.search(r'\bwe\s+is\b', text_lower):
        errors += 1
    if re.search(r'\bthey\s+is\b', text_lower):
        errors += 1
    
    # Multiple spaces (weak indicator but counts)
    multiple_spaces = len(re.findall(r'  {2,}', transcript))
    if multiple_spaces > 3:
        errors += 1
    
    # Very fragmented sentences (fragments < 2 words after period are usually errors)
    sentences = re.split(r'[.!?]+', transcript)
    single_word_fragments = 0
    for sentence in sentences:
        words = sentence.strip().split()
        if len(words) == 1 and words[0].lower() not in ['yes', 'no', 'ok', 'thanks', 'great', 'nice', 'well']:
            single_word_fragments += 1
    
    if single_word_fragments > 2:
        errors += 1
    
    # Avoid over-penalizing: cap errors estimate
    # This is intentionally conservative to avoid punishing natural speech
    return min(errors, 3)  # Max 3 errors detected to keep scoring fair

def score_grammar(transcript: str) -> dict:
    """
    Score grammar using formula: Grammar Score = 1 - min(errors per 100 words / 10, 1)
    >0.9: 10 pts
    0.7-0.89: 8 pts
    0.5-0.69: 6 pts
    0.3-0.49: 4 pts
    <0.3: 2 pts
    """
    word_count = len(re.findall(r'\b\w+\b', transcript))
    
    if word_count == 0:
        return {
            'grammar': 0,
            'total': 0,
            'feedback': "Cannot calculate grammar score",
            'metrics': {'error_rate': 0, 'errors': 0}
        }
    
    errors = count_grammar_errors(transcript)
    errors_per_100 = (errors / word_count) * 100
    
    # Formula from rubric: 1 - min(errors_per_100_words / 10, 1)
    grammar_score_raw = 1 - min(errors_per_100 / 10, 1)
    
    if grammar_score_raw >= 0.9:
        score = 10
        level = "Excellent"
    elif grammar_score_raw >= 0.7:
        score = 8
        level = "Very Good"
    elif grammar_score_raw >= 0.5:
        score = 6
        level = "Good"
    elif grammar_score_raw >= 0.3:
        score = 4
        level = "Fair"
    else:
        score = 2
        level = "Poor"
    
    feedback = f"Grammar: {level} ({errors} errors found, {errors_per_100:.2f} errors per 100 words)"
    
    return {
        'grammar': score,
        'total': score,
        'feedback': feedback,
        'metrics': {
            'error_rate': grammar_score_raw,
            'errors': errors,
            'errors_per_100': errors_per_100
        }
    }

def score_language_grammar(transcript: str) -> dict:
    """Aggregate language and grammar scores"""
    grammar_result = score_grammar(transcript)
    vocabulary_result = score_vocabulary_richness(transcript)
    
    total_score = grammar_result['grammar'] + vocabulary_result['vocabulary']
    
    return {
        'grammar': grammar_result['grammar'],
        'vocabulary': vocabulary_result['vocabulary'],
        'total': total_score,
        'feedback': {
            'grammar': grammar_result['feedback'],
            'vocabulary': vocabulary_result['feedback']
        },
        'metrics': {
            'grammar': grammar_result['metrics'],
            'vocabulary': vocabulary_result['metrics']
        }
    }
