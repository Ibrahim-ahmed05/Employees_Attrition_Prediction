@echo off
echo Starting both FastAPI servers...
echo.

echo Starting ML Prediction API (main.py) on port 8000...
start "ML Prediction API" cmd /k "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak > nul

echo Starting Supabase API (test.py) on port 8001...
start "Supabase API" cmd /k "uvicorn test:app --host 0.0.0.0 --port 8001 --reload"

echo.
echo Both servers are starting...
echo ML Prediction API: http://localhost:8000
echo Supabase API: http://localhost:8001
echo.
echo Press any key to exit...
pause > nul
