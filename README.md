# PROSPECTIA

A comprehensive CRM web application for commercial prospect management.

## Features

- User authentication and authorization (JWT-based)
- Role-based access control (ADMIN, COMMERCIAL, MANAGER)
- Company and prospect management
- Contact management linked to prospects
- Activity tracking (calls, meetings, emails, etc.)
- Follow-up scheduling with reminders
- Prospect conversion tracking
- AI-powered prospect evaluation (with local fallback)
- Dashboard with metrics and charts
- Prospect qualification and scoring system
- Activities timeline view
- Follow-ups management with calendar
- Reports module with filtering and CSV export
- User management interface (admin only)
- Responsive design with Tailwind CSS
- API documentation with Swagger
- Dockerized for easy deployment

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLAlchemy 2.0 with SQLite (development), configurable to PostgreSQL/MySQL
- **Authentication**: JWT (python-jose) with bcrypt password hashing
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **Testing**: Pytest

### Frontend
- **Framework**: React 18 with Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context / hooks (or Redux/TBD)
- **Data Fetching**: Axios
- **Charts**: Recharts
- **Icons**: Lucide React
- **Routing**: React Router DOM

## Getting Started

### Prerequisites
- Docker and Docker Compose (for containerized deployment)
- OR
- Python 3.11+ and Node.js 18+ (for local development)

### Option 1: Using Docker Compose (Recommended)
1. Clone the repository
2. Run `docker compose up --build`
3. The backend will be available at `http://localhost:8000`
4. The frontend will be available at `http://localhost:3000`

### Option 2: Local Development
#### Backend
1. Navigate to the `backend` directory
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables (copy `.env.example` to `.env` and adjust)
6. Run the database migrations: `alembic upgrade head`
7. Start the server: `uvicorn app.main:app --reload`
8. The API will be available at `http://localhost:8000`

#### Frontend
1. Navigate to the `frontend` directory
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. The frontend will be available at `http://localhost:5173` (Vite default)

### Seeding Demo Data
To populate the database with demo data:
```bash
# Backend
cd backend
python seed.py
```

## API Documentation
Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing
### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
*(To be implemented)*
```bash
cd frontend
npm test
```

## Deployment
The application is designed to be deployed using Docker Compose. For production, consider:
- Using a production-grade database (PostgreSQL/MySQL)
- Setting strong SECRET_KEY and environment variables
- Using a reverse proxy (NGINX) for SSL termination
- Configuring proper restart policies

## Project Structure
```
PROSPECTIA/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── api.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   ├── prospect.py
│   │   │   ├── contact.py
│   │   │   ├── activity.py
│   │   │   ├── follow_up.py
│   │   │   ├── conversion.py
│   │   │   └── ai_evaluation.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   ├── prospect.py
│   │   │   ├── contact.py
│   │   │   ├── activity.py
│   │   │   ├── follow_up.py
│   │   │   ├── conversion.py
│   │   │   └── ai_evaluation.py
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── company_service.py
│   │   │   ├── prospect_service.py
│   │   │   ├── contact_service.py
│   │   │   ├── activity_service.py
│   │   │   ├── follow_up_service.py
│   │   │   ├── conversion_service.py
│   │   │   ├── ai_evaluation_service.py
│   │   │   └── ai_service.py
│   │   ├── routers/
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   ├── prospect.py
│   │   │   ├── contact.py
│   │   │   ├── activity.py
│   │   │   ├── follow_up.py
│   │   │   ├── conversion.py
│   │   │   └── ai_evaluation.py
│   │   ├── main.py
│   │   └── seed.py
│   ├── tests/
│   │   └── test_user.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ...
│   │   ├── App.tsx
│   │   ├── index.css
│   │   └── main.tsx
│   ├── public/
│   │   └── index.html
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.cjs
│   └── postcss.config.cjs
├── docker-compose.yml
└README.md
```

## Environment Variables
The backend uses the following environment variables (see `.env.example`):

- `DATABASE_URL`: Database connection string (default: SQLite)
- `SECRET_KEY`: Secret key for JWT signing
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration time
- `AI_PROVIDER`: AI provider to use (`none` for fallback, or `openai` for OpenAI API)
- `AI_API_KEY`: API key for the AI provider (if applicable)

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Inspired by various CRM systems
- Built with FastAPI and React
- Thanks to the open-source community