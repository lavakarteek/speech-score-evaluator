import re

FILLER_WORDS = [
    'um', 'uh', 'like', 'you know', 'so', 'actually', 'basically', 
    'right', 'i mean', 'well', 'kinda', 'sort of', 'okay', 'hmm', 'ah',
    'erm', 'er', 'aah'
]

def count_filler_words(transcript: str) -> int:
    """Count filler words in transcript"""
    text_lower = transcript.lower()
    filler_count = 0
    
    for filler in FILLER_WORDS:
        # Use word boundaries for single words, but allow flexibility for phrases
        if ' ' in filler:
            # For multi-word fillers like "you know", "i mean"
            pattern = r'\b' + filler.replace(' ', r'\s+') + r'\b'
        else:
            # For single word fillers
            pattern = r'\b' + filler + r'\b'
        
        matches = re.findall(pattern, text_lower)
        filler_count += len(matches)
    
    return filler_count

def calculate_filler_word_rate(transcript: str) -> tuple:
    """
    Calculate filler word rate
    Rate = (Number of filler words / Total words) * 100
    """
    words = re.findall(r'\b\w+\b', transcript)
    total_words = len(words)
    
    if total_words == 0:
        return 0, 0
    
    filler_count = count_filler_words(transcript)
    rate = (filler_count / total_words) * 100
    
    return rate, filler_count

def score_clarity(transcript: str) -> dict:
    """
    Score clarity based on filler word rate (0-15 points)
    0-3%: 15 pts
    4-6%: 12 pts
    7-9%: 9 pts
    10-12%: 6 pts
    13%+: 3 pts
    """
    rate, filler_count = calculate_filler_word_rate(transcript)
    
    if rate <= 3:
        score = 15
        level = "Excellent"
    elif rate <= 6:
        score = 12
        level = "Very Good"
    elif rate <= 9:
        score = 9
        level = "Good"
    elif rate <= 12:
        score = 6
        level = "Fair"
    else:
        score = 3
        level = "Poor"
    
    feedback = f"Clarity: {level} - Filler word rate: {rate:.2f}% ({filler_count} filler words)"
    
    return {
        'filler_words': score,
        'total': score,
        'feedback': feedback,
        'metrics': {
            'filler_word_rate': rate,
            'filler_count': filler_count,
            'total_words': len(re.findall(r'\b\w+\b', transcript))
        }
    }
