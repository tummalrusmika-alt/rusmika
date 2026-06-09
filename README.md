# Local Problem Reporter App

A comprehensive platform for citizens to report local issues (potholes, garbage, broken streetlights) with photo verification, voice input in local languages, and automatic routing to authorities.

## Features

✅ Photo Upload & Verification (AI-powered)
✅ Voice Reporting in Local Languages (Hindi, Tamil, Telugu, Kannada, Marathi, Bengali)
✅ Duplicate Complaint Detection
✅ Severity Scoring
✅ Before/After Repair Photos
✅ Live Complaint Tracking
✅ Automatic Routing to Departments
✅ Community Upvotes for Urgent Issues
✅ Email Notifications
✅ Geolocation Support

## Tech Stack

### Backend
- **Framework**: Python + FastAPI
- **Database**: SQLite (development) / PostgreSQL (production)
- **AI/ML**: OpenCV, TensorFlow Lite (image verification)
- **Email**: SMTP (Gmail)
- **Voice Processing**: Google Speech-to-Text API
- **Geolocation**: Geopy

### Frontend
- **Framework**: React
- **Styling**: Tailwind CSS
- **State Management**: Redux
- **Voice Recording**: react-mic
- **Map**: Leaflet.js
- **Internationalization**: i18next

## Project Structure

```
local-problem-reporter/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── config.py
│   ├── models.py
│   ├── database.py
│   ├── routes/
│   │   ├── complaints.py
│   │   ├── users.py
│   │   ├── auth.py
│   │   └── admin.py
│   ├── utils/
│   │   ├── email_service.py
│   │   ├── image_processor.py
│   │   ├── voice_processor.py
│   │   └── geolocation.py
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── locales/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── .env.example
└── docs/
    ├── SETUP.md
    ├── API.md
    └── DEPLOYMENT.md
```

## Quick Start

See [SETUP.md](docs/SETUP.md) for detailed setup instructions.

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Email Configuration

Complaints are sent to: `tummalrusmika@gmail.com`

See [SETUP.md](docs/SETUP.md) for Gmail setup instructions.

## Local Languages Supported

- 🇮🇳 Hindi (हिंदी)
- 🇮🇳 Tamil (தமிழ்)
- 🇮🇳 Telugu (తెలుగు)
- 🇮🇳 Kannada (ಕನ್ನಡ)
- 🇮🇳 Marathi (मराठी)
- 🇮🇳 Bengali (বাংলা)

## License

MIT License
