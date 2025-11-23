# Speech Score Evaluator

A comprehensive tool for evaluating student self-introductions based on a detailed rubric using Python, Streamlit, and SQLite.

## Features

✅ **Automated Speech Evaluation** - Scores introductions across 8 different criteria
✅ **SQLite Database** - Stores all evaluations for history and analytics
✅ **Interactive Streamlit UI** - User-friendly interface for evaluating speeches
✅ **Detailed Feedback** - Comprehensive breakdown of scores and suggestions
✅ **Visual Analytics** - Radar charts and statistics dashboard
✅ **Validation & Error Handling** - Robust input validation to prevent edge cases

## Scoring Rubric (100 points total)

### 1. Content & Structure (40 points)
- **Salutation Level** (5 pts): Greeting quality assessment
  - Excellent (5): "I am excited to introduce" / "Feeling great"
  - Good (4): "Good Morning/Afternoon/Evening", "Hello everyone"
  - Normal (2): "Hi", "Hello"
  - None (0): No salutation

- **Keyword Presence** (30 pts): Essential information included
  - Must-have (20 pts): Name, Age, School/Class, Family, Hobbies
  - Good-to-have (10 pts): Origin, Goals, Unique facts, Strengths

- **Flow** (5 pts): Logical structure
  - Excellent (5): Salutation → Name → Details → Optional → Closing
  - Partial (3): Most elements present but out of order
  - Poor (0): Disorganized

### 2. Speech Rate (10 points)
- **WPM Calculation**: (Word Count / Duration in seconds) × 60
  - Ideal (10 pts): 111-140 WPM
  - Fast (6 pts): 141-160 WPM
  - Slow (6 pts): 81-110 WPM
  - Too Fast (2 pts): >161 WPM
  - Too Slow (2 pts): <80 WPM

### 3. Language & Grammar (20 points)
- **Grammar** (10 pts): Error detection
  - Formula: 1 − min(errors per 100 words / 10, 1)
  - >0.9: 10 pts | 0.7-0.89: 8 pts | 0.5-0.69: 6 pts | 0.3-0.49: 4 pts | <0.3: 2 pts

- **Vocabulary Richness** (10 pts): Type-Token Ratio (TTR)
  - TTR = Distinct words / Total words
  - 0.9-1.0: 10 pts | 0.7-0.89: 8 pts | 0.5-0.69: 6 pts | 0.3-0.49: 4 pts | 0-0.29: 2 pts

### 4. Clarity (15 points)
- **Filler Word Rate**: (Filler words / Total words) × 100
  - 0-3%: 15 pts | 4-6%: 12 pts | 7-9%: 9 pts | 10-12%: 6 pts | 13%+: 3 pts
  - Filler words: um, uh, like, you know, so, actually, basically, right, etc.

### 5. Engagement (15 points)
- **Sentiment Analysis**: VADER sentiment score
  - ≥0.9: 15 pts | 0.7-0.89: 12 pts | 0.5-0.69: 9 pts | 0.3-0.49: 6 pts | <0.3: 3 pts

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Navigate to project**
   ```powershell
   cd d:\nirmaan_speech_score
   ```

2. **Activate virtual environment** (Already configured with all dependencies)
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   If this is a fresh copy, create virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

## Usage

### Running the Streamlit App

With virtual environment activated:
```powershell
streamlit run app.py
```

Or use the full path directly:
```powershell
D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py
```

The app will open in your browser at `http://localhost:8501`

**Note:** On first run, wait 10-15 seconds for the server to fully initialize. If you see "site can't be reached", refresh the page.

### Features in the UI

1. **📝 Evaluate Speech** - Input transcript and get detailed scoring
2. **📊 View Results** - See history of all evaluations
3. **📈 Statistics** - View aggregate statistics across evaluations

### Example Evaluation

**Input:**
```
Student Name: Muskan
Word Count: 131
Sentence Count: 11
Duration: 52 seconds
Transcript: "Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School..."
```

**Output:**
- Total Score: 86/100
- Detailed breakdown of each criterion
- Visual radar chart
- Feedback for improvement

## Project Structure

```
d:\nirmaan_speech_score\
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── database.py                     # SQLite database operations
├── content_scoring.py              # Content & structure scoring
├── speech_rate_scoring.py          # Speech rate calculation
├── language_grammar_scoring.py     # Grammar & vocabulary scoring
├── clarity_scoring.py              # Filler word detection
├── engagement_scoring.py           # Sentiment analysis
├── validation.py                   # Input validation & sanitization
├── test_scoring.py                 # Full test suite
├── quick_test.py                   # Quick validation test
└── speech_scores.db                # SQLite database (auto-created)
```

## Module Details

### `database.py`
- Initializes SQLite schema
- Stores transcripts, scores, and metrics
- Provides query functions for retrieval and analytics

### `content_scoring.py`
- Detects salutation level
- Extracts and scores keywords using flexible regex patterns
- Evaluates structural flow
- **Anti-overfitting**: Multiple pattern matching to handle various phrasings

### `speech_rate_scoring.py`
- Calculates WPM from word count and duration
- Maps to rubric scoring brackets
- **Anti-overfitting**: Uses standard WPM calculation, not tuned to specific data

### `language_grammar_scoring.py`
- Conservative grammar error detection
- Calculates TTR for vocabulary richness
- **Anti-overfitting**: Limits error detection to obvious issues only

### `clarity_scoring.py`
- Detects filler words from comprehensive list
- Calculates filler word rate percentage
- **Anti-overfitting**: Uses predefined filler word list, not custom-trained

### `engagement_scoring.py`
- Uses VADER sentiment analysis (industry-standard library)
- Returns sentiment probability score
- **Anti-overfitting**: Leverages pre-trained VADER, no custom tuning

### `validation.py`
- Validates all inputs (name, transcript, duration, etc.)
- Provides sanitization
- Prevents edge cases and malformed data

## Design Decisions

### 1. **Anti-Overfitting Approach**
- Pattern matching is flexible with multiple alternatives for each criterion
- Grammar detection is conservative (only counts obvious errors)
- Uses industry-standard libraries (VADER, TTR) rather than custom models
- Validation prevents edge cases that might skew scoring

### 2. **Database Choice (SQLite)**
- Lightweight, no external server needed
- Embedded directly in application
- Perfect for this use case (single-user or small team)
- Easy deployment and backup

### 3. **Streamlit Framework**
- Rapid UI development without front-end complexity
- Interactive components for data input
- Built-in plotting capabilities
- Easy to modify and extend

### 4. **Modular Architecture**
- Each scoring criterion in separate module
- Easy to update individual scoring logic
- Facilitates testing and maintenance
- Clear separation of concerns

## Testing

### Run Test Suite
```bash
python test_scoring.py
```

### Quick Validation
```bash
python quick_test.py
```

### Expected Results (Sample Data)
- Word Count: 131
- Duration: 52 seconds
- Expected Score: ~86/100

## Deployment

### Option 1: Local Deployment
```bash
streamlit run app.py
```

### Option 2: Streamlit Cloud
1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Connect GitHub repository
4. Deploy

### Option 3: Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

## Extensibility

### Adding New Scoring Criteria
1. Create new module (e.g., `pronunciation_scoring.py`)
2. Implement scoring function
3. Import and integrate in `app.py`
4. Update database schema if needed

### Integrating Real NLP Tools
- Replace TTR with MTLD (more sophisticated)
- Use Language Tool Python for grammar (more accurate)
- Integrate speech-to-text if audio input is needed

## Known Limitations

1. **Grammar Detection**: Uses pattern matching, not a full grammar parser
2. **Sentiment Analysis**: Works on transcript text, not audio tone/emotion
3. **Manual Metrics**: Word count, sentence count, and duration are user-provided
4. **No Speech Recognition**: Requires pre-transcribed text

## Future Improvements

- [ ] Upload audio and auto-generate transcript using speech-to-text
- [ ] Integrate Language Tool Python for better grammar detection
- [ ] Add MTLD calculation for more sophisticated vocabulary analysis
- [ ] Export results to PDF
- [ ] Multi-language support
- [ ] Rubric customization interface
- [ ] Batch evaluation from CSV
- [ ] Export database to Excel

## License

This project is created for Nirmaan Education.

## Support

For issues or questions, contact: jassmesh@nirmaan.education

## Version

**Speech Score Evaluator v1.0**
- Initial release with 5 scoring criteria
- SQLite database integration
- Streamlit UI with analytics
