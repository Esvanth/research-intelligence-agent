@echo off
echo.
echo ===============================================
echo   Research Intelligence Agent
echo   Agents League Hackathon 2026 - Foundry IQ
echo ===============================================
echo.

if not exist .env (
  echo ERROR: .env file not found!
  echo.
  echo Run this first:
  echo   copy .env.example .env
  echo Then open .env and fill in your Azure credentials.
  echo.
  pause
  exit /b 1
)

if not exist frontend\node_modules (
  echo Installing frontend dependencies...
  cd frontend
  call npm install
  cd ..
)

echo Starting FastAPI backend on http://localhost:8000
start "RIA Backend" cmd /k "python app.py"

timeout /t 3 /nobreak > nul

echo Starting React frontend on http://localhost:5173
echo.
echo ===============================================
echo   Open browser at: http://localhost:5173
echo   Close both terminal windows to stop
echo ===============================================
echo.

cd frontend
call npm run dev
