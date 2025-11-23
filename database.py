import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "speech_scores.db"

def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Create transcripts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            transcript TEXT NOT NULL,
            word_count INTEGER,
            sentence_count INTEGER,
            duration_seconds INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create scores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transcript_id INTEGER NOT NULL,
            salutation_score REAL,
            keyword_presence_score REAL,
            flow_score REAL,
            speech_rate_score REAL,
            grammar_score REAL,
            vocabulary_score REAL,
            filler_word_score REAL,
            sentiment_score REAL,
            total_score REAL,
            detailed_feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (transcript_id) REFERENCES transcripts(id)
        )
    ''')
    
    # Create evaluation metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluation_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score_id INTEGER NOT NULL,
            metric_name TEXT,
            metric_value REAL,
            FOREIGN KEY (score_id) REFERENCES scores(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_transcript(student_name, transcript, word_count, sentence_count, duration_seconds):
    """Save transcript to database"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO transcripts (student_name, transcript, word_count, sentence_count, duration_seconds)
        VALUES (?, ?, ?, ?, ?)
    ''', (student_name, transcript, word_count, sentence_count, duration_seconds))
    
    conn.commit()
    transcript_id = cursor.lastrowid
    conn.close()
    
    return transcript_id

def save_score(transcript_id, scores_dict, feedback):
    """Save score to database"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO scores 
        (transcript_id, salutation_score, keyword_presence_score, flow_score, 
         speech_rate_score, grammar_score, vocabulary_score, filler_word_score, 
         sentiment_score, total_score, detailed_feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        transcript_id,
        scores_dict.get('salutation', 0),
        scores_dict.get('keyword_presence', 0),
        scores_dict.get('flow', 0),
        scores_dict.get('speech_rate', 0),
        scores_dict.get('grammar', 0),
        scores_dict.get('vocabulary', 0),
        scores_dict.get('filler_words', 0),
        scores_dict.get('sentiment', 0),
        scores_dict.get('total', 0),
        json.dumps(feedback)
    ))
    
    conn.commit()
    score_id = cursor.lastrowid
    conn.close()
    
    return score_id

def get_all_transcripts():
    """Retrieve all transcripts with their scores"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT t.id, t.student_name, t.created_at, s.total_score
        FROM transcripts t
        LEFT JOIN scores s ON t.id = s.transcript_id
        ORDER BY t.created_at DESC
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_transcript_details(transcript_id):
    """Get transcript and score details by ID"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT t.*, s.*
        FROM transcripts t
        LEFT JOIN scores s ON t.id = s.transcript_id
        WHERE t.id = ?
    ''', (transcript_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return result

def get_statistics():
    """Get overall statistics"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM transcripts')
    total_transcripts = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(total_score) FROM scores')
    avg_score = cursor.fetchone()[0]
    
    cursor.execute('SELECT MAX(total_score) FROM scores')
    max_score = cursor.fetchone()[0]
    
    cursor.execute('SELECT MIN(total_score) FROM scores')
    min_score = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_transcripts': total_transcripts,
        'average_score': avg_score,
        'max_score': max_score,
        'min_score': min_score
    }
