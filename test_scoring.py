"""
Test script to verify scoring logic with sample data
"""

from content_scoring import score_content_structure
from speech_rate_scoring import score_speech_rate
from language_grammar_scoring import score_language_grammar
from clarity_scoring import score_clarity
from engagement_scoring import score_engagement

# Sample transcript from case study
sample_transcript = """Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. 
I am 13 years old. I live with my family. There are 3 people in my family, me, my mother and my father.
One special thing about my family is that they are very kind hearted to everyone and soft spoken. One thing I really enjoy is play, playing cricket and taking wickets.
A fun fact about me is that I see in mirror and talk by myself. One thing people don't know about me is that I once stole a toy from one of my cousin.
 My favorite subject is science because it is very interesting. Through science I can explore the whole world and make the discoveries and improve the lives of others. 
Thank you for listening."""

word_count = 131
sentence_count = 11
duration_seconds = 52

print("=" * 70)
print("SPEECH EVALUATION TEST - SAMPLE DATA")
print("=" * 70)
print(f"\nStudent: Muskan")
print(f"Word Count: {word_count}")
print(f"Sentence Count: {sentence_count}")
print(f"Duration: {duration_seconds} seconds")
print("\nTranscript Preview:")
print(sample_transcript[:200] + "...")

print("\n" + "=" * 70)
print("SCORING BREAKDOWN")
print("=" * 70)

# Content & Structure (max 40)
content_scores = score_content_structure(sample_transcript)
print(f"\n1. CONTENT & STRUCTURE (Target: 40)")
print(f"   - Salutation: {content_scores['salutation']}/5")
print(f"   - Keyword Presence: {content_scores['keyword_presence']}/30")
print(f"   - Flow: {content_scores['flow']}/5")
print(f"   - Total: {content_scores['total']}/40")
print(f"   Feedback: {content_scores['feedback']}")

# Speech Rate (max 10)
speech_rate_scores = score_speech_rate(word_count, duration_seconds)
print(f"\n2. SPEECH RATE (Target: 10)")
print(f"   - WPM: {speech_rate_scores['metrics']['wpm']:.1f}")
print(f"   - Score: {speech_rate_scores['speech_rate']}/10")
print(f"   Feedback: {speech_rate_scores['feedback']}")

# Language & Grammar (max 20)
language_scores = score_language_grammar(sample_transcript)
print(f"\n3. LANGUAGE & GRAMMAR (Target: 20)")
print(f"   - Grammar: {language_scores['grammar']}/10")
print(f"   - Vocabulary (TTR): {language_scores['vocabulary']}/10")
print(f"   - Total: {language_scores['total']}/20")
print(f"   Grammar Feedback: {language_scores['feedback']['grammar']}")
print(f"   Vocabulary Feedback: {language_scores['feedback']['vocabulary']}")

# Clarity (max 15)
clarity_scores = score_clarity(sample_transcript)
print(f"\n4. CLARITY (Target: 15)")
print(f"   - Filler Word Rate: {clarity_scores['metrics']['filler_word_rate']:.2f}%")
print(f"   - Score: {clarity_scores['filler_words']}/15")
print(f"   Feedback: {clarity_scores['feedback']}")

# Engagement (max 15)
engagement_scores = score_engagement(sample_transcript)
print(f"\n5. ENGAGEMENT (Target: 15)")
print(f"   - Sentiment Score: {engagement_scores['metrics']['sentiment_score']:.3f}")
print(f"   - Score: {engagement_scores['sentiment']}/15")
print(f"   Feedback: {engagement_scores['feedback']}")

# Calculate total
content_total = content_scores['total']
speech_total = speech_rate_scores['speech_rate']
language_total = language_scores['total']
clarity_total = clarity_scores['filler_words']
engagement_total = engagement_scores['sentiment']

# Scale to weightage
content_scaled = (content_total / 40) * 40
speech_scaled = (speech_total / 10) * 10
language_scaled = (language_total / 20) * 20
clarity_scaled = (clarity_total / 15) * 15
engagement_scaled = (engagement_total / 15) * 15

total_score = content_scaled + speech_scaled + language_scaled + clarity_scaled + engagement_scaled

print("\n" + "=" * 70)
print("FINAL RESULTS")
print("=" * 70)
print(f"\nContent & Structure:    {content_scaled:.1f}/40")
print(f"Speech Rate:            {speech_scaled:.1f}/10")
print(f"Language & Grammar:     {language_scaled:.1f}/20")
print(f"Clarity:                {clarity_scaled:.1f}/15")
print(f"Engagement:             {engagement_scaled:.1f}/15")
print(f"\n{'TOTAL SCORE':.<40} {total_score:.1f}/100")
print("=" * 70)

# Expected: 86/100
print(f"\nExpected Score (from rubric): 86/100")
print(f"Achieved Score: {total_score:.1f}/100")
print(f"Difference: {abs(total_score - 86):.1f} points")
