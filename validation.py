"""
Input validation and sanitization module
Ensures robustness and prevents edge case failures
"""

def validate_transcript(transcript: str) -> tuple:
    """
    Validate transcript input
    Returns: (is_valid, error_message)
    """
    if not transcript or not isinstance(transcript, str):
        return False, "Transcript must be a non-empty string"
    
    if len(transcript.strip()) < 10:
        return False, "Transcript too short (minimum 10 characters)"
    
    if len(transcript) > 50000:
        return False, "Transcript too long (maximum 50,000 characters)"
    
    return True, ""

def validate_student_name(name: str) -> tuple:
    """
    Validate student name
    Returns: (is_valid, error_message)
    """
    if not name or not isinstance(name, str):
        return False, "Student name must be a non-empty string"
    
    if len(name.strip()) < 2:
        return False, "Student name too short"
    
    if len(name) > 100:
        return False, "Student name too long"
    
    return True, ""

def validate_duration(duration: int) -> tuple:
    """
    Validate duration in seconds
    Returns: (is_valid, error_message)
    """
    if not isinstance(duration, (int, float)):
        return False, "Duration must be a number"
    
    if duration <= 0:
        return False, "Duration must be positive"
    
    if duration > 3600:  # Max 1 hour
        return False, "Duration exceeds maximum (1 hour)"
    
    return True, ""

def validate_word_count(word_count: int) -> tuple:
    """
    Validate word count
    Returns: (is_valid, error_message)
    """
    if not isinstance(word_count, int):
        return False, "Word count must be an integer"
    
    if word_count < 1:
        return False, "Word count must be at least 1"
    
    if word_count > 10000:
        return False, "Word count exceeds maximum (10,000 words)"
    
    return True, ""

def validate_sentence_count(sentence_count: int) -> tuple:
    """
    Validate sentence count
    Returns: (is_valid, error_message)
    """
    if not isinstance(sentence_count, int):
        return False, "Sentence count must be an integer"
    
    if sentence_count < 1:
        return False, "Sentence count must be at least 1"
    
    if sentence_count > 1000:
        return False, "Sentence count exceeds maximum (1,000 sentences)"
    
    return True, ""

def sanitize_transcript(transcript: str) -> str:
    """
    Sanitize transcript: remove extra whitespace but preserve content
    """
    # Remove extra whitespace while preserving paragraph structure
    lines = transcript.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(cleaned_lines)
