# Quick Command Reference

## Local Development

### Run (Recommended - Direct Path)
```powershell
cd d:\nirmaan_speech_score
D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py
```

### Or With Activation
```powershell
cd d:\nirmaan_speech_score
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

### If ExecutionPolicy Error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

### Access App
```
http://localhost:8501
```

**Note:** Virtual environment includes all dependencies (streamlit, plotly, pandas, nltk, etc.)

---

## Testing

### Run Full Test Suite
```bash
python test_scoring.py
```

### Quick Validation
```bash
python quick_test.py
```

---

## Docker Deployment

### Build & Run
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f
```

### Stop
```bash
docker-compose down
```

### Access
```
http://localhost:8501
```

---

## Database Management

### Backup Database
```bash
cp speech_scores.db speech_scores_backup_$(date +%Y%m%d_%H%M%S).db
```

### Check Database Integrity
```bash
sqlite3 speech_scores.db "PRAGMA integrity_check;"
```

### Optimize Database
```bash
sqlite3 speech_scores.db "VACUUM;"
```

---

## Troubleshooting

### Check if Port 8501 is in Use (Windows)
```powershell
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### Reinstall Dependencies (If Needed)
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt --upgrade
```

### Clear Streamlit Cache
```powershell
Remove-Item -Path "$env:APPDATA\.streamlit\cache" -Recurse -Force
```

### "Site can't be reached" Error
- Try: http://192.168.1.5:8501 (local network IP)
- Wait 10-15 seconds for server to initialize
- Refresh the page (Ctrl+R)

---

## Project Files Summary

```
Core Application Files:
├── app.py                        # Main Streamlit app
├── database.py                   # SQLite operations
├── content_scoring.py            # Content scoring (40 pts)
├── speech_rate_scoring.py        # Speech rate scoring (10 pts)
├── language_grammar_scoring.py   # Language scoring (20 pts)
├── clarity_scoring.py            # Clarity scoring (15 pts)
├── engagement_scoring.py         # Engagement scoring (15 pts)
├── validation.py                 # Input validation

Configuration & Deployment:
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image config
├── docker-compose.yml            # Docker Compose config
├── .streamlit/config.toml        # Streamlit config
├── .gitignore                    # Git ignore rules

Documentation:
├── README.md                     # Main documentation
├── DEPLOYMENT.md                 # Deployment guide
├── PROJECT_SUMMARY.md            # Project overview
├── QUICK_REFERENCE.md            # This file

Testing:
├── test_scoring.py               # Full test suite
├── quick_test.py                 # Quick validation

Database:
└── speech_scores.db              # SQLite database (auto-created)
```

---

## Sample Workflow

### 1. Start Development
```bash
cd d:\nirmaan_speech_score
pip install -r requirements.txt
streamlit run app.py
```

### 2. Test Application
```bash
# In another terminal
python test_scoring.py
```

### 3. Deploy with Docker
```bash
docker-compose up -d
# Access at http://localhost:8501
```

### 4. Backup Data
```bash
cp speech_scores.db backup/speech_scores_$(date).db
```

---

## Important Notes

⚠️ **Before First Run**
- Ensure Python 3.8+ is installed
- Run: `pip install -r requirements.txt`
- Database will auto-initialize

⚠️ **ExecutionPolicy Error (Windows)**
- Problem: "running scripts is disabled on this system"
- Solution: Use direct path: `D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py`
- Or fix policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force`

⚠️ **Module Not Found Error**
- Problem: "No module named 'plotly'" or similar
- Solution: Make sure you're using virtual environment Python
- Use: `D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py`

⚠️ **NLTK Data**
- First time using engagement scoring, NLTK will download data
- Requires internet connection
- Can be pre-downloaded: `python -c "import nltk; nltk.download('vader_lexicon')"`

⚠️ **Port Conflicts**
- Default port is 8501
- Check if port is free: `netstat -ano | findstr :8501`
- Change port: `D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py --server.port 8502`

⚠️ **Database Backups**
- Always backup before updates
- SQLite database stores in `speech_scores.db`
- Database is persistent across app restarts

---

## Performance Tips

### For Local Development
- First load may take 5-10 seconds
- Subsequent loads are faster (cached)
- Database operations are lightweight

### For Production
- Use Docker for consistent environment
- Monitor disk space for database growth
- Implement regular backups (cron job)
- Consider database indexing for large datasets

---

## Support

**For Issues:**
1. Check if all packages installed: `pip list`
2. Verify Python version: `python --version`
3. Check port availability: `netstat -ano | findstr :8501`
4. View Streamlit logs for errors

**Contact:** jassmesh@nirmaan.education

---

**Last Updated:** November 23, 2025
**Version:** 1.0
**Status:** Production Ready ✅
