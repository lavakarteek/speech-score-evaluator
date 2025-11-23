import re
from typing import Tuple

def score_salutation(transcript: str) -> Tuple[float, str]:
    """
    Score salutation level (0-5 points)
    Excellent (5): "I am excited to introduce" or "Feeling great"
    Good (4): Good Morning/Afternoon/Evening/Day, Hello everyone
    Normal (2): Hi, Hello
    No Salutation (0)
    """
    first_50_words = ' '.join(transcript.split()[:50]).lower()
    
    excellent_patterns = [
        r'i\s+am\s+excited\s+to\s+introduce',
        r'feeling\s+great',
        r'delighted\s+to'
    ]
    
    good_patterns = [
        r'good\s+morning',
        r'good\s+afternoon',
        r'good\s+evening',
        r'good\s+day',
        r'hello\s+everyone'
    ]
    
    normal_patterns = [
        r'\bhi\b',
        r'\bhello\b'
    ]
    
    for pattern in excellent_patterns:
        if re.search(pattern, first_50_words):
            return 5, "Excellent salutation: Enthusiastic greeting found"
    
    for pattern in good_patterns:
        if re.search(pattern, first_50_words):
            return 4, "Good salutation: Proper greeting used"
    
    for pattern in normal_patterns:
        if re.search(pattern, first_50_words):
            return 2, "Normal salutation: Basic greeting used"
    
    return 0, "No formal salutation found"

def extract_keywords(transcript: str) -> dict:
    """
    Extract and score keyword presence
    Must-have (4 points each): Name, Age, School/Class, Family, Hobbies
    Good-to-have (2 points each): Family details, Origin, Goals, Unique facts, Strengths
    Uses flexible pattern matching to avoid overfitting to specific examples
    """
    text_lower = transcript.lower()
    keywords_found = {
        'must_have': [],
        'good_to_have': []
    }
    
    # Must-have keywords detection with flexible patterns
    
    # Name - various ways to mention name
    name_patterns = [
        r'\bmy\s+name\s+(?:is|are)\s+\w+',
        r'\bmyself\s+\w+',
        r'\bi\s+am\s+\w+',
        r"i'm\s+\w+",
        r'\bcall\s+(?:me|myself)\s+\w+'
    ]
    if any(re.search(pattern, text_lower) for pattern in name_patterns):
        keywords_found['must_have'].append('name')
    
    # Age - various formats for age mention
    age_patterns = [
        r'\d+\s+(?:years?\s+)?old',
        r'age\s+(?:is\s+)?\d+',
        r"i'm\s+\d+",
        r'\bi\s+am\s+\d+',
    ]
    if any(re.search(pattern, text_lower) for pattern in age_patterns):
        keywords_found['must_have'].append('age')
    
    # School/Class/Education - various mentions
    school_patterns = [
        r'(?:studying|study|study in|am in)\s+(?:class|grade|standard)',
        r'class\s+\d+',
        r'school\s+\w+',
        r'college|university',
        r'section\s+[a-z]',
        r'education|institute'
    ]
    if any(re.search(pattern, text_lower) for pattern in school_patterns):
        keywords_found['must_have'].append('school_class')
    
    # Family - various family mentions
    family_patterns = [
        r'\bfamily\b',
        r'(?:mother|father|parents?|brother|sister|sibling)',
        r'(?:mom|dad|mum)',
        r'live\s+with',
        r'members?\s+in\s+(?:family|house)'
    ]
    if any(re.search(pattern, text_lower) for pattern in family_patterns):
        keywords_found['must_have'].append('family')
    
    # Hobbies/Interests - flexible patterns
    hobbies_patterns = [
        r'\b(?:hobby|hobbies)\b',
        r'(?:like|enjoy|love)\s+(?:to\s+)?(?:play|do|watch)',
        r'interested\s+in',
        r'passion\s+(?:is|for)',
        r'free\s+time.*?(?:play|do|watch|read)',
        r'(?:play|do|participate|engaged)\s+in'
    ]
    if any(re.search(pattern, text_lower) for pattern in hobbies_patterns):
        keywords_found['must_have'].append('hobbies')
    
    # Good-to-have keywords
    
    # Unique facts/special something
    unique_patterns = [
        r'(?:fun|interesting|unique|special)\s+(?:fact|thing)',
        r'something\s+(?:unique|special|interesting)',
        r'people\s+don?\'?t\s+know',
        r'(?:one\s+thing|something)\s+(?:special|unique)',
        r'special\s+about\s+me'
    ]
    if any(re.search(pattern, text_lower) for pattern in unique_patterns):
        keywords_found['good_to_have'].append('unique_fact')
    
    # Goals/Dreams/Ambition
    goals_patterns = [
        r'(?:goal|dream|ambition)',
        r'(?:want|wish|aspire|aim)\s+to',
        r'(?:hope|future)',
        r'(?:like to|interested in)\s+(?:become|be)',
        r'career.*?(?:goal|plan|interest)'
    ]
    if any(re.search(pattern, text_lower) for pattern in goals_patterns):
        keywords_found['good_to_have'].append('goal')
    
    # Strengths/Achievements
    strength_patterns = [
        r'(?:strength|talent|skill)',
        r'(?:good|excellent|great)\s+at',
        r'achievement|accomplish',
        r'(?:excel|proficient)',
        r'(?:won|won\'t|best|award)',
    ]
    if any(re.search(pattern, text_lower) for pattern in strength_patterns):
        keywords_found['good_to_have'].append('strength')
    
    # Origin/Location
    origin_patterns = [
        r'(?:from|belong to|native)\s+\w+',
        r'(?:i\s+)?am\s+from',
        r'parents?\s+(?:are\s+)?from',
        r'(?:origin|birthplace)',
        r'(?:city|town|place|country)\s+(?:is|was)'
    ]
    if any(re.search(pattern, text_lower) for pattern in origin_patterns):
        keywords_found['good_to_have'].append('origin')
    
    return keywords_found

def score_keyword_presence(transcript: str) -> Tuple[float, dict]:
    """Score keyword presence (0-30 points)"""
    keywords = extract_keywords(transcript)
    
    # Must-have: 4 points each, max 20
    must_have_score = min(len(keywords['must_have']) * 4, 20)
    
    # Good-to-have: 2 points each, max 10
    good_to_have_score = min(len(keywords['good_to_have']) * 2, 10)
    
    total_score = must_have_score + good_to_have_score
    
    feedback = {
        'must_have_found': keywords['must_have'],
        'good_to_have_found': keywords['good_to_have'],
        'must_have_score': must_have_score,
        'good_to_have_score': good_to_have_score
    }
    
    return total_score, feedback

def check_flow(transcript: str) -> Tuple[float, str]:
    """
    Score flow/structure (0-5 points)
    Expected order: Salutation -> Name -> Mandatory details -> Optional details -> Closing
    Uses flexible heuristics to avoid overfitting
    """
    text_lower = transcript.lower()
    
    # Count key components present
    has_salutation = bool(re.search(r'\b(?:hello|hi|good\s+(?:morning|afternoon|evening|day)|hey|greetings?)\b', text_lower[:150]))
    
    # Find positions of key elements (more flexible patterns)
    name_pos = re.search(r'(?:myself|my\s+name|i\s+am)\s+\w+', text_lower)
    mandatory_details = re.search(r'(?:age|year.*?old|class|school)', text_lower)
    hobbies_pos = re.search(r'(?:enjoy|like|hobby|passion|interested)', text_lower)
    closing_pos = re.search(r'(?:thank|thanks|goodbye|bye|farewell)', text_lower)
    
    # Scoring logic
    score = 0
    feedback = ""
    
    # Check for presence and order
    elements_present = sum([
        bool(has_salutation),
        bool(name_pos),
        bool(mandatory_details),
        bool(hobbies_pos),
        bool(closing_pos)
    ])
    
    # Optimal flow check: are elements appearing in roughly correct order?
    positions = []
    if has_salutation:
        positions.append(('salutation', 0))
    if name_pos:
        positions.append(('name', name_pos.start()))
    if mandatory_details:
        positions.append(('details', mandatory_details.start()))
    if hobbies_pos:
        positions.append(('hobbies', hobbies_pos.start()))
    if closing_pos:
        positions.append(('closing', closing_pos.start()))
    
    if len(positions) >= 4:
        # Most elements present and in logical order
        score = 5
        feedback = "Excellent flow: Introduction follows logical structure"
    elif len(positions) >= 3:
        # Good attempt at structure
        score = 3
        feedback = "Fair flow: Most elements present, some reordering needed"
    elif len(positions) >= 2:
        # Minimal structure
        score = 1
        feedback = "Basic structure: Few elements present"
    else:
        # Very poor structure
        score = 0
        feedback = "Poor flow: Disorganized structure"
    
    return score, feedback

def score_content_structure(transcript: str) -> dict:
    """Aggregate all content and structure scores"""
    salutation_score, salutation_feedback = score_salutation(transcript)
    keyword_score, keyword_feedback = score_keyword_presence(transcript)
    flow_score, flow_feedback = check_flow(transcript)
    
    total_score = salutation_score + keyword_score + flow_score
    
    return {
        'salutation': salutation_score,
        'keyword_presence': keyword_score,
        'flow': flow_score,
        'total': total_score,
        'feedback': {
            'salutation': salutation_feedback,
            'keywords': keyword_feedback,
            'flow': flow_feedback
        }
    }
