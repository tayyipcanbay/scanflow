@echo off
echo ========================================
echo 3D Body Progress Engine - Frontend Starter
echo ========================================
echo.

cd frontend
echo Installing dependencies (if needed)...
call npm install

echo.
echo Starting frontend development server...
echo.
echo Frontend will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause

