# AI Interview Twin 🎯

An AI-powered interview assistant that helps candidates prepare for tech interviews by providing real-time feedback and personalized improvement recommendations.

## 🌟 Features

- **Role-Based Interviews**: Select from multiple tech roles (Software Engineer, Data Analyst, Cloud Engineer, etc.)
- **AI-Powered Questions**: Dynamic question generation based on the selected role
- **Multi-Modal Input**: Support for both text and voice answers
- **Real-Time Evaluation**: Instant scoring across multiple dimensions:
  - Technical Correctness
  - Communication Quality
  - Confidence Level
- **Detailed Feedback**: Personalized strengths, weaknesses, and improvement roadmap
- **Interview History**: Track your progress across multiple interviews

## 🏗️ Project Structure

```text
AI Interview Twin/
├── frontend/                 # Next.js React application
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── pages/           # Next.js pages (routing)
│   │   ├── services/        # API services & state management
│   │   ├── styles/          # Global styles & Tailwind config
│   │   └── utils/           # Helper functions
│   ├── package.json         # Frontend dependencies
│   ├── next.config.js       # Next.js configuration
│   ├── tsconfig.json        # TypeScript configuration
│   └── tailwind.config.js   # Tailwind CSS configuration
│
├── backend/                  # FastAPI Python application
│   ├── app/
│   │   ├── main.py          # FastAPI application entry point
│   │   ├── models/          # SQLAlchemy models & Pydantic schemas
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic & AI integration
│   │   ├── database/        # Database configuration
│   │   └── config/          # Settings and configuration
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile           # Container configuration
│   └── .env.example         # Environment variables template
│
├── docker-compose.yml       # Docker compose for local development
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ (for frontend)
- Python 3.11+ (for backend)
- PostgreSQL 16 (or use Docker)
- OpenAI API Key or Gemini API Key

### 1. Clone and Setup

```bash
git clone <repository-url>
cd "AI Interview Twin"
```

### 2. Environment Configuration

#### Backend (.env)

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys
```

#### Frontend (.env.local)

```bash
cp frontend/.env.example frontend/.env.local
```

### 3. Using Docker (Recommended)

```bash
# Start all services (PostgreSQL + Backend)
docker-compose up -d

# Frontend runs separately
cd frontend
npm install
npm run dev
```

The application will be available at:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000](http://localhost:8000)
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Manual Setup (Without Docker)

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 📊 API Endpoints

### Interview Management

- `POST /api/interviews/start` - Start a new interview
- `GET /api/interviews/{interview_id}` - Get interview details
- `GET /api/interviews/{interview_id}/questions` - Get interview questions
- `POST /api/interviews/{interview_id}/end` - End interview session

### Evaluation

- `POST /api/evaluations/evaluate` - Evaluate an answer
- `GET /api/evaluations/{interview_id}/summary` - Get interview summary

### User Management

- `POST /api/users/register` - Register a new user
- `GET /api/users/{user_id}` - Get user profile

## 🤖 AI Integration

The system integrates with:

- **OpenAI GPT API**: For question generation and answer evaluation
- **Google Gemini API**: Alternative AI provider
- **Web Speech API**: Browser-based voice input

### Adding AI Integration

1. Update `backend/app/services/ai_service.py` with your API calls
2. Implement `generate_questions()` and `evaluate_answer()` methods
3. Add API keys to `.env` file

## 🎨 Frontend Features

### Components

- **RoleSelector**: Role selection interface
- **QuestionCard**: Question display with text/voice input
- **ResultCard**: Individual question evaluation results

### Pages

- `/` - Home page with role selector
- `/interview/[interviewId]` - Interview interface
- `/results/[interviewId]` - Interview results and summary

## 🔧 Technology Stack

| Category | Technology |
| --- | --- |
| Frontend | Next.js, React, Tailwind CSS |
| Backend | FastAPI, Python |
| Database | PostgreSQL |
| State Management | Zustand |
| API Client | Axios |
| UI Notifications | React Hot Toast |
| Speech | Web Speech API / Whisper |
| AI | OpenAI / Google Gemini |

## 📝 Database Schema

### Tables

- **interviews**: Interview sessions
- **questions**: Interview questions
- **answers**: User answers
- **evaluations**: Individual answer evaluations
- **interview_results**: Final interview summary

## 🔐 Environment Variables

### Backend

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/db
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
SECRET_KEY=your-secret-key
DEBUG=True/False
```

### Frontend

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 Development Guide

### Adding a New Interview Role

1. Update `roles` in `frontend/src/components/RoleSelector.jsx`
2. Add role-specific questions in `backend/app/services/interview_service.py`
3. Customize evaluation criteria if needed

### Customizing Evaluation Logic

Edit `backend/app/services/evaluation_service.py` to modify scoring logic and feedback generation.

### Styling

The project uses Tailwind CSS. Modify `frontend/tailwind.config.js` for customization.

## 🚢 Deployment

### Frontend (Vercel)

```bash
npm run build
vercel deploy
```

### Backend (Heroku / Railway)

```bash
docker build -t ai-interview-backend .
# Push to registry and deploy
```

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit changes (`git commit -m 'Add AmazingFeature'`)
3. Push to branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🎓 Future Enhancements

- [ ] User authentication and profiles
- [ ] Interview history and analytics
- [ ] Real-time score visualization
- [ ] Industry-specific role templates
- [ ] Video recording of interviews
- [ ] Peer comparison analytics
- [ ] Scheduled practice sessions
- [ ] Integration with job portals

## 🆘 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres
```

### API Connection Issues

```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/app/main.py
```

### Frontend Build Issues

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Built with love for tech interview preparation
