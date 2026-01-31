# 3D Body Progress Engine

A system that takes time-series 3D body mesh uploads, compares geometry over time, and visually highlights body changes with color-coded heatmaps.

## Features

- 🟢 **Green** → decrease (fat loss / volume reduction)
- 🔴 **Red** → increase (muscle gain / volume increase)
- Interactive 3D visualization
- AI-generated insights
- Personalized meal and training plans

## Architecture

- **Backend**: FastAPI (Python) with mesh processing and comparison
- **Frontend**: React + Three.js for 3D visualization
- **Database**: SQLite (development) / PostgreSQL (production)
- **Storage**: Local filesystem for mesh files

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `POST /api/upload` - Upload 3D mesh file
- `GET /api/comparison/{baseline_id}/{comparison_id}` - Get comparison results
- `GET /api/insights/{comparison_id}` - Get AI-generated insights
- `GET /api/actions/{user_id}` - Get personalized action plans

## Project Structure

```
3d-body-progress-engine/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
└── tests/            # Test files
```

