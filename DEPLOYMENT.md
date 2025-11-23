# Deployment Guide - Speech Score Evaluator

## Quick Start (Local Development)

### Method 1: Direct Path (Recommended - No Activation Needed)
```powershell
cd d:\nirmaan_speech_score
D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py
```

### Method 2: With Activation
```powershell
cd d:\nirmaan_speech_score
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

### If ExecutionPolicy Error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

**Access:** Open browser to `http://localhost:8501`

**Note:** Virtual environment (.venv) is already configured with all dependencies installed

---

## Deployment Options

### Option 1: Windows Local Deployment

**Requirements:**
- Python 3.12 (already installed)
- Windows PowerShell 5.1 or higher
- Virtual environment (.venv) - **ALREADY INCLUDED**

**Steps - Direct Path Method:**
```powershell
cd d:\nirmaan_speech_score
D:\nirmaan_speech_score\.venv\Scripts\streamlit.exe run app.py
```

**Steps - With Activation:**
```powershell
# Fix ExecutionPolicy if needed (one-time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Navigate to project
cd d:\nirmaan_speech_score

# Activate the included virtual environment
.\.venv\Scripts\Activate.ps1

# Run the app
streamlit run app.py
```

**Access:** Open browser to `http://localhost:8501`

**If this is a fresh copy:**
```powershell
cd d:\nirmaan_speech_score
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

**Streamlit Config:** Fixed in `.streamlit/config.toml` for compatibility

### Option 2: Docker Deployment (Recommended for Production)

**Requirements:**
- Docker Desktop installed
- docker-compose (included with Docker Desktop)

**Steps:**

1. **Build and run with Docker Compose:**
   ```bash
   cd d:\nirmaan_speech_score
   docker-compose up -d
   ```

2. **Access the app:**
   - Open browser to `http://localhost:8501`

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the app:**
   ```bash
   docker-compose down
   ```

**Database Persistence:**
- SQLite database is persisted in volume mount
- Data survives container restarts

---

### Option 3: Streamlit Cloud (Free Hosting)

**Requirements:**
- GitHub account
- GitHub repository with project code

**Steps:**

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/speech-score-evaluator.git
   git push -u origin main
   ```

2. **Visit Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repository
   - Select `app.py` as the main file
   - Deploy!

**URL Pattern:** `https://<username>-speech-score-evaluator-<random>.streamlit.app`

---

### Option 4: Heroku Deployment

**Requirements:**
- Heroku CLI installed
- Heroku account

**Steps:**

1. **Create `Procfile` in project root:**
   ```
   web: streamlit run --server.port $PORT app.py
   ```

2. **Deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

3. **Access:** `https://your-app-name.herokuapp.com`

---

### Option 5: AWS Deployment

**Using EC2:**

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t2.micro or larger

2. **Install on EC2:**
   ```bash
   ssh -i key.pem ubuntu@your-instance-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3-pip git -y
   
   # Clone repository
   git clone https://github.com/yourusername/speech-score-evaluator.git
   cd speech-score-evaluator
   
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Run app with nohup (background)
   nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > app.log 2>&1 &
   ```

3. **Configure Security Group:**
   - Allow inbound traffic on port 8501
   - Restrict to your IP for security

4. **Access:** `http://your-instance-ip:8501`

---

### Option 6: Using Ngrok for External Access

**For testing without full deployment:**

1. **Install Ngrok:** https://ngrok.com/download

2. **Run Streamlit locally:**
   ```bash
   streamlit run app.py
   ```

3. **In another terminal, expose with Ngrok:**
   ```bash
   ngrok http 8501
   ```

4. **Share the public URL** from Ngrok output

---

## Database Backup

### Backup SQLite Database

```bash
# Copy database to backup location
cp speech_scores.db speech_scores_backup_$(date +%Y%m%d_%H%M%S).db

# Or use Python script for automated backups
python backup_db.py
```

### Create `backup_db.py`:
```python
import shutil
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy('speech_scores.db', f'backups/speech_scores_{timestamp}.db')
    print(f"Database backed up: backups/speech_scores_{timestamp}.db")

if __name__ == "__main__":
    backup_database()
```

---

## Environment Variables

### For production, create `.env` file:
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_LOGGER_LEVEL=info
```

### Load in app with:
```python
import os
from dotenv import load_dotenv

load_dotenv()
port = os.getenv('STREAMLIT_SERVER_PORT', 8501)
```

---

## Performance Optimization

### For high traffic:

1. **Use caching:**
   ```python
   @st.cache_data
   def cached_function():
       return get_all_transcripts()
   ```

2. **Database indexing:**
   ```sql
   CREATE INDEX idx_student_name ON transcripts(student_name);
   CREATE INDEX idx_created_at ON scores(created_at);
   ```

3. **Load balancing** (for multiple instances):
   - Use Nginx as reverse proxy
   - Run multiple app instances

---

## Monitoring & Maintenance

### Check App Health
```bash
# Docker
docker-compose ps

# Local
curl http://localhost:8501/_stcore/health
```

### View Logs
```bash
# Docker
docker-compose logs -f speech-evaluator

# Local
# Logs appear in terminal where app is running
```

### Database Maintenance
```bash
# Backup before maintenance
python backup_db.py

# Vacuum database (optimize)
sqlite3 speech_scores.db "VACUUM;"

# Check database integrity
sqlite3 speech_scores.db "PRAGMA integrity_check;"
```

---

## Troubleshooting

### Issue: "Port 8501 already in use"
```bash
# Find and kill process using port 8501
# Windows:
netstat -ano | findstr :8501

# Linux/Mac:
lsof -i :8501
kill -9 <PID>
```

### Issue: "nltk.sentiment not found"
```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

### Issue: Database locked
- Check if another instance is running
- Stop all instances and restart

### Issue: Streamlit Cloud import errors
- Add `packages.txt` with system dependencies
- Or use `requirements.txt` with full specifications

---

## Security Best Practices

1. **Enable HTTPS**
   - Use Nginx/Apache reverse proxy with SSL
   - Get certificate from Let's Encrypt

2. **Authentication**
   - Add Streamlit authentication
   - Or use cloud provider's built-in auth

3. **Database Security**
   - Regular backups
   - Restrict file permissions
   - Consider encryption for sensitive data

4. **Input Validation**
   - Already implemented in `validation.py`
   - Sanitize all user inputs

5. **Environment Variables**
   - Don't commit secrets to Git
   - Use `.env` files (add to `.gitignore`)

---

## Support & Further Help

- **Streamlit Docs:** https://docs.streamlit.io
- **Docker Docs:** https://docs.docker.com
- **Heroku Docs:** https://devcenter.heroku.com
- **AWS EC2 Guide:** https://aws.amazon.com/ec2

---

**Last Updated:** November 23, 2025
