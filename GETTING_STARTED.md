# Getting Started Guide

## 🚀 30-Second Quickstart

### Windows PowerShell (Direct Method - Recommended)
```powershell
cd d:\nirmaan_speech_score
D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py
```

### Or with Activation (if ExecutionPolicy allows)
```powershell
cd d:\nirmaan_speech_score
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

### If ExecutionPolicy Error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

### Then Open
```
http://localhost:8501
```

Done! 🎉

**Note:** Virtual environment (.venv) is already set up with all dependencies.

---

## 📋 What You Need

- **Python 3.8+** (Check: `python --version`)
- **pip** (Usually comes with Python)
- **~5 minutes** for first setup
- **~30MB** disk space

---

## 🔧 Detailed Setup

### Step 1: Navigate to Project
```powershell
cd d:\nirmaan_speech_score
```

### Step 2: Activate Virtual Environment (Already Set Up)

If you get an ExecutionPolicy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

Then:
```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Run the App

**Option A: With Activation (after Step 2)**
```powershell
streamlit run app.py
```

**Option B: Direct Path (Skip Step 2, use anytime)**
```powershell
D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py
```

### Step 4: Open Browser
Visit: `http://localhost:8501`

**Note:** All dependencies (streamlit, nltk, pandas, plotly, etc.) are pre-installed in the virtual environment.

---

## 📝 Using the App

### Tab 1: Evaluate Speech
1. **Enter Student Name** (e.g., "Muskan")
2. **Enter Duration** (seconds the speech took)
3. **Enter Word Count** (total words in transcript)
4. **Enter Sentence Count** (total sentences)
5. **Paste Transcript** (the speech text)
6. **Click "Evaluate Speech"**
7. **Get Results!** Score breakdown appears instantly

### Tab 2: View Results
- See history of all evaluated speeches
- View scores for each student

### Tab 3: Statistics
- Average score across all evaluations
- Highest and lowest scores
- Total number of evaluations

---

## 📊 Understanding Your Score

### Score Breakdown (100 points total)

| Criteria | Points | What It Measures |
|----------|--------|------------------|
| Content | 40 | Did they introduce themselves properly? |
| Speech Rate | 10 | Did they speak at the right pace? |
| Language | 20 | Grammar and vocabulary quality |
| Clarity | 15 | How many filler words (um, uh, like)? |
| Engagement | 15 | How positive and enthusiastic? |

### Example Score
```
Muskan's Introduction:
- Content: 31/40 (Good)
- Speech Rate: 6/10 (A bit fast)
- Language: 16/20 (Very good)
- Clarity: 15/15 (Excellent)
- Engagement: 12/15 (Good)
────────────────
Total: ~80/100 (Very Good!)
```

---

## 🐛 Troubleshooting

### Problem: "Port 8501 already in use"
**Solution:**
```bash
# Change port
streamlit run app.py --server.port 8502
```

### Problem: "nltk.sentiment not found"
**Solution:**
```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

### Problem: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "ExecutionPolicy" Error
**Error Message:**
```
cannot be loaded because running scripts is disabled on this system
```

**Solution Option 1: Use Direct Path (Recommended)**
```powershell
D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py
```
No activation needed - this bypasses the policy restriction entirely.

**Solution Option 2: Fix Execution Policy**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

### Problem: Database "locked"
**Solution:**
- Close all instances of the app
- Wait 5 seconds
- Restart: `D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py`

### Problem: "No module named 'streamlit'"
**Solution:**
This means the wrong Python is running. Use:
```powershell
D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py
```

---

## 💾 Data Management

### Database Location
```
d:\nirmaan_speech_score\speech_scores.db
```

### Backup Your Data
```bash
# Create backup
cp speech_scores.db speech_scores_backup.db

# Or on Windows:
copy speech_scores.db speech_scores_backup.db
```

---

## 🐳 Using Docker (Optional)

### Quick Start with Docker
```bash
docker-compose up -d
```

### Access
```
http://localhost:8501
```

### Stop
```bash
docker-compose down
```

---

## 📚 Sample Transcript to Try

```
Hello everyone, my name is John. I am 14 years old and I study in class 9 at Delhi Public School. 
I live with my parents and my younger sister. My family is very supportive and loving.
In my free time, I love playing cricket and reading books. I am very interested in science 
and hope to become a scientist one day. A unique thing about me is that I am a national-level 
chess player. Thank you for listening!
```

**Expected Score:** 75-85/100

---

## 🎯 Tips for Better Scores

### Content (40 pts)
✅ Start with a greeting ("Hello everyone")
✅ Mention your name clearly
✅ Tell your age and school
✅ Talk about your family
✅ Share your hobbies
✅ End with "Thank you"

### Speech Rate (10 pts)
✅ Speak at 111-140 words per minute
✅ Not too fast, not too slow
✅ Clear and steady pace

### Language (20 pts)
✅ Use correct grammar
✅ Avoid repeated words
✅ Use variety in vocabulary

### Clarity (15 pts)
✅ Avoid filler words: "um", "uh", "like", "you know"
✅ Speak clearly without hesitations

### Engagement (15 pts)
✅ Sound positive and enthusiastic
✅ Express gratitude
✅ Show confidence

---

## 📖 Documentation

### For More Info
- **README.md** - Full documentation
- **DEPLOYMENT.md** - How to deploy online
- **QUICK_REFERENCE.md** - Command reference
- **PROJECT_SUMMARY.md** - What the project does

### View Documentation
```bash
# In VS Code
code README.md

# Or open any .md file in your editor
```

---

## ✅ Verification Checklist

Before first use, verify:
- [ ] Python installed: `python --version`
- [ ] pip works: `pip --version`
- [ ] In correct folder: `cd d:\nirmaan_speech_score`
- [ ] Requirements installed: `pip list | grep streamlit`
- [ ] NLTK data downloaded: `python -c "import nltk; nltk.data.find('sentiment')"`
- [ ] App runs: `streamlit run app.py` (no errors)
- [ ] Browser opens to localhost:8501

---

## 🆘 Still Stuck?

### Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Site can't be reached" | Wait 10s and refresh, or try http://192.168.1.5:8501 |
| "Port 8501 in use" | Run: `netstat -ano \| findstr :8501` then `taskkill /PID <PID> /F` |
| "Module not found" | Activate venv: `.\.venv\Scripts\Activate.ps1` then reinstall |
| "Streamlit not found" | Use full path: `D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py` |
| "Blank page loading" | Reload page (Ctrl+R) and wait for app to initialize |

### Virtual Environment Issues
```powershell
# Reactivate if needed
.\.venv\Scripts\Activate.ps1

# Reinstall all packages
pip install -r requirements.txt --upgrade
```

### Get Help
- Check **IMPLEMENTATION_REPORT.md**
- Review **DEPLOYMENT.md**
- Contact: jassmesh@nirmaan.education

---

## 🎉 You're Ready!

```bash
cd d:\nirmaan_speech_score
pip install -r requirements.txt
streamlit run app.py
```

Visit `http://localhost:8501` and start evaluating! 

---

**Happy Evaluating! 🎤**

**Last Updated:** November 23, 2025
