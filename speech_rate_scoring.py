def calculate_speech_rate(word_count: int, duration_seconds: int) -> tuple:
    """
    Calculate speech rate in WPM (words per minute)
    Too Fast: >161 WPM (2 pts)
    Fast: 141-160 WPM (6 pts)
    Ideal: 111-140 WPM (10 pts)
    Slow: 81-110 WPM (6 pts)
    Too Slow: <80 WPM (2 pts)
    """
    if duration_seconds == 0:
        return 0, "Duration not provided"
    
    wpm = (word_count / duration_seconds) * 60
    
    if wpm > 161:
        return 2, f"Too fast: {wpm:.1f} WPM (ideal: 111-140)"
    elif 141 <= wpm <= 160:
        return 6, f"Fast: {wpm:.1f} WPM (ideal: 111-140)"
    elif 111 <= wpm <= 140:
        return 10, f"Ideal: {wpm:.1f} WPM"
    elif 81 <= wpm <= 110:
        return 6, f"Slow: {wpm:.1f} WPM (ideal: 111-140)"
    else:  # < 80
        return 2, f"Too slow: {wpm:.1f} WPM (ideal: 111-140)"

def score_speech_rate(word_count: int, duration_seconds: int) -> dict:
    """Aggregate speech rate scoring"""
    score, feedback = calculate_speech_rate(word_count, duration_seconds)
    
    return {
        'speech_rate': score,
        'total': score,
        'feedback': feedback,
        'metrics': {
            'wpm': (word_count / duration_seconds) * 60 if duration_seconds > 0 else 0,
            'word_count': word_count,
            'duration_seconds': duration_seconds
        }
    }
