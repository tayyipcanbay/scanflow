@echo off
echo ========================================
echo 3D Body Progress Engine - Server Starter
echo ========================================
echo.

cd backend
echo Starting FastAPI server...
echo.
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause

