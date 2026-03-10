# Placement Portal Application

## Project Overview
The Placement Portal Application is a full-stack web application designed to streamline the campus recruitment process. It replaces manual spreadsheet tracking by providing a centralized platform for the Institute Admin, Companies, and Students to manage registrations, job drives, and applications.

## 🚀 Placement Portal V2 - Setup Guide

### Backend Setup

#### 1. Navigate to the Directory
Open your WSL terminal and move to the project folder:
```bash
cd "/mnt/c/Users/singh/Placement Portal/placement-portal-v2/backend"
```

#### 2. Environment Configuration
Create and activate a virtual environment to manage dependencies:
```bash
python3 -m venv .celery
source .celery/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install "celery[redis]"
```

#### 5. Start Celery Worker
```bash
celery -A app.celery_app worker --loglevel=info
```

#### 6. Start Celery Beat Scheduler
```bash
celery -A app.celery_app beat --loglevel=info
```

#### 7. Start Redis Server (WSL)
```bash
redis-server
```

#### 8. Run Flask Application
```bash
python app.py
```

#### 9. Run Mailhog (WSL)
```bash
mailhog
```

---

### 🎨 Frontend Configuration

#### 1. Navigate to Frontend Directory
```bash
cd frontend
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Start Development Server
```bash
npm run dev
```

---

#### ✅ Services Required

Make sure the following services are running:

- Redis Server
- Celery Worker
- Celery Beat
- Flask Backend
- Mailhog
- Vue Frontend Dev Server