import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path
import traceback

# Add project to path
project_path = Path(__file__).parent
sys.path.insert(0, str(project_path))

from database import init_db, save_transcript, save_score, get_all_transcripts, get_statistics
from content_scoring import score_content_structure
from speech_rate_scoring import score_speech_rate
from language_grammar_scoring import score_language_grammar
from clarity_scoring import score_clarity
from engagement_scoring import score_engagement
from validation import (
    validate_transcript, validate_student_name, validate_duration,
    validate_word_count, validate_sentence_count, sanitize_transcript
)

# Initialize database
init_db()

# Page config
st.set_page_config(
    page_title="Speech Score Evaluator",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎤 Speech Score Evaluator")
st.markdown("*A comprehensive tool for evaluating student self-introductions based on rubric criteria*")

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    ["📝 Evaluate Speech", "📊 View Results", "📈 Statistics"]
)

def evaluate_speech():
    """Page for evaluating a new speech"""
    st.header("📝 Evaluate Student Speech")
    
    with st.form("evaluation_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            student_name = st.text_input("Student Name *", placeholder="Enter student name")
        with col2:
            duration_seconds = st.number_input("Duration (seconds) *", min_value=1, value=52)
        
        transcript = st.text_area(
            "Transcript *",
            placeholder="Paste the speech transcript here...",
            height=200
        )
        
        col1, col2 = st.columns(2)
        with col1:
            word_count = st.number_input("Word Count *", min_value=1, value=131)
        with col2:
            sentence_count = st.number_input("Sentence Count *", min_value=1, value=11)
        
        submit_button = st.form_submit_button("🎯 Evaluate Speech", use_container_width=True)
        
        if submit_button:
            # Validate all inputs
            name_valid, name_error = validate_student_name(student_name)
            transcript_valid, transcript_error = validate_transcript(transcript)
            duration_valid, duration_error = validate_duration(duration_seconds)
            word_valid, word_error = validate_word_count(word_count)
            sentence_valid, sentence_error = validate_sentence_count(sentence_count)
            
            if not name_valid:
                st.error(f"❌ Student Name: {name_error}")
                return
            if not transcript_valid:
                st.error(f"❌ Transcript: {transcript_error}")
                return
            if not duration_valid:
                st.error(f"❌ Duration: {duration_error}")
                return
            if not word_valid:
                st.error(f"❌ Word Count: {word_error}")
                return
            if not sentence_valid:
                st.error(f"❌ Sentence Count: {sentence_error}")
                return
            
            # Show evaluation in progress
            with st.spinner("🔄 Evaluating speech..."):
                try:
                    # Sanitize transcript
                    transcript = sanitize_transcript(transcript)
                    
                    # Save transcript to database
                    transcript_id = save_transcript(
                        student_name, transcript, word_count, sentence_count, duration_seconds
                    )
                    
                    # Calculate scores
                    content_scores = score_content_structure(transcript)
                    speech_rate_scores = score_speech_rate(word_count, duration_seconds)
                    language_scores = score_language_grammar(transcript)
                    clarity_scores = score_clarity(transcript)
                    engagement_scores = score_engagement(transcript)
                    
                    # Combine all scores
                    all_scores = {
                        'salutation': content_scores['salutation'],
                        'keyword_presence': content_scores['keyword_presence'],
                        'flow': content_scores['flow'],
                        'speech_rate': speech_rate_scores['speech_rate'],
                        'grammar': language_scores['grammar'],
                        'vocabulary': language_scores['vocabulary'],
                        'filler_words': clarity_scores['filler_words'],
                        'sentiment': engagement_scores['sentiment']
                    }
                    
                    # Calculate total score based on weightage
                    # Content & Structure: 40 (5+30+5)
                    # Speech Rate: 10
                    # Language & Grammar: 20 (10+10)
                    # Clarity: 15
                    # Engagement: 15
                    
                    content_total = content_scores['salutation'] + content_scores['keyword_presence'] + content_scores['flow']
                    language_total = language_scores['grammar'] + language_scores['vocabulary']
                    
                    # Scale each section to their weightage
                    content_scaled = (content_total / 40) * 40  # Already out of 40
                    speech_rate_scaled = (speech_rate_scores['speech_rate'] / 10) * 10
                    language_scaled = (language_total / 20) * 20
                    clarity_scaled = (clarity_scores['filler_words'] / 15) * 15
                    engagement_scaled = (engagement_scores['sentiment'] / 15) * 15
                    
                    total_score = content_scaled + speech_rate_scaled + language_scaled + clarity_scaled + engagement_scaled
                    
                    all_scores['total'] = total_score
                    
                    # Prepare feedback
                    feedback = {
                        'content': content_scores['feedback'],
                        'speech_rate': speech_rate_scores['feedback'],
                        'language': language_scores['feedback'],
                        'clarity': clarity_scores['feedback'],
                        'engagement': engagement_scores['feedback']
                    }
                    
                    # Save score to database
                    save_score(transcript_id, all_scores, feedback)
                    
                    # Display results
                    st.success("✅ Evaluation Complete!")
                    
                    # Score display with visual
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Score", f"{total_score:.1f}/100")
                    with col2:
                        st.metric("Content & Structure", f"{content_scaled:.1f}/40")
                    with col3:
                        st.metric("Language & Grammar", f"{language_scaled:.1f}/20")
                    with col4:
                        st.metric("Other Factors", f"{clarity_scaled + engagement_scaled:.1f}/30")
                    
                    # Detailed breakdown
                    st.subheader("📊 Detailed Score Breakdown")
                    
                    breakdown_data = {
                        'Criteria': [
                            'Salutation',
                            'Keyword Presence',
                            'Flow',
                            'Speech Rate',
                            'Grammar',
                            'Vocabulary',
                            'Filler Words',
                            'Sentiment/Engagement'
                        ],
                        'Score': [
                            content_scores['salutation'],
                            content_scores['keyword_presence'],
                            content_scores['flow'],
                            speech_rate_scores['speech_rate'],
                            language_scores['grammar'],
                            language_scores['vocabulary'],
                            clarity_scores['filler_words'],
                            engagement_scores['sentiment']
                        ],
                        'Max Score': [5, 30, 5, 10, 10, 10, 15, 15]
                    }
                    
                    df_breakdown = pd.DataFrame(breakdown_data)
                    st.dataframe(df_breakdown, use_container_width=True)
                    
                    # Feedback details
                    st.subheader("💬 Detailed Feedback")
                    
                    feedback_cols = st.columns(2)
                    with feedback_cols[0]:
                        st.write("**Content & Structure:**")
                        st.write(f"- Salutation: {content_scores['feedback']['salutation']}")
                        st.write(f"- Keywords: {content_scores['feedback']['keywords']}")
                        st.write(f"- Flow: {content_scores['feedback']['flow']}")
                    
                    with feedback_cols[1]:
                        st.write("**Language & Clarity:**")
                        st.write(f"- Grammar: {language_scores['feedback']['grammar']}")
                        st.write(f"- Vocabulary: {language_scores['feedback']['vocabulary']}")
                        st.write(f"- Clarity: {clarity_scores['feedback']}")
                    
                    st.write("**Engagement:**")
                    st.write(f"- Sentiment: {engagement_scores['feedback']}")
                    
                    # Metrics
                    st.subheader("📈 Detailed Metrics")
                    metrics_col1, metrics_col2 = st.columns(2)
                    
                    with metrics_col1:
                        st.write("**Speech Metrics:**")
                        st.write(f"- WPM: {speech_rate_scores['metrics']['wpm']:.1f}")
                        st.write(f"- Word Count: {word_count}")
                        st.write(f"- Duration: {duration_seconds}s")
                    
                    with metrics_col2:
                        st.write("**Language Metrics:**")
                        st.write(f"- TTR (Vocabulary): {language_scores['metrics']['vocabulary']['ttr']:.3f}")
                        st.write(f"- Grammar Error Rate: {language_scores['metrics']['grammar']['errors_per_100']:.2f}%")
                        st.write(f"- Filler Word Rate: {clarity_scores['metrics']['filler_word_rate']:.2f}%")
                    
                    # Visualization
                    fig = go.Figure(data=[
                        go.Scatterpolar(
                            r=[
                                content_scores['salutation'],
                                content_scores['keyword_presence'],
                                content_scores['flow'],
                                speech_rate_scores['speech_rate'],
                                language_scores['grammar'],
                                language_scores['vocabulary'],
                                clarity_scores['filler_words'],
                                engagement_scores['sentiment']
                            ],
                            theta=[
                                'Salutation',
                                'Keywords',
                                'Flow',
                                'Speech Rate',
                                'Grammar',
                                'Vocabulary',
                                'Clarity',
                                'Engagement'
                            ],
                            fill='toself',
                            name='Score'
                        )
                    ])
                    
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 30])),
                        title="Score Radar Chart",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"❌ Error during evaluation: {str(e)}")
                    with st.expander("Technical Details"):
                        st.code(traceback.format_exc())

def view_results():
    """Page to view previous evaluations"""
    st.header("📊 View Evaluation Results")
    
    transcripts = get_all_transcripts()
    
    if not transcripts:
        st.info("No evaluations yet. Go to 'Evaluate Speech' to get started!")
        return
    
    # Create DataFrame
    df = pd.DataFrame(
        transcripts,
        columns=['ID', 'Student Name', 'Created At', 'Score']
    )
    
    st.dataframe(df, use_container_width=True)
    
    st.info("Note: Detailed view of individual results coming soon!")

def view_statistics():
    """Page to view overall statistics"""
    st.header("📈 Overall Statistics")
    
    stats = get_statistics()
    
    if stats['total_transcripts'] == 0:
        st.info("No data yet. Evaluate some speeches to see statistics!")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Evaluations", stats['total_transcripts'])
    with col2:
        st.metric("Average Score", f"{stats['average_score']:.1f}" if stats['average_score'] else "N/A")
    with col3:
        st.metric("Highest Score", f"{stats['max_score']:.1f}" if stats['max_score'] else "N/A")
    with col4:
        st.metric("Lowest Score", f"{stats['min_score']:.1f}" if stats['min_score'] else "N/A")

# Route pages
if page == "📝 Evaluate Speech":
    evaluate_speech()
elif page == "📊 View Results":
    view_results()
elif page == "📈 Statistics":
    view_statistics()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p><small>Speech Score Evaluator v1.0 | Powered by Streamlit & SQLite</small></p>
    </div>
    """,
    unsafe_allow_html=True
)
