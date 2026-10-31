#!/bin/bash
set -e

echo "=========================================================="
echo " Starting Healix Platform (Backend & Frontend Dev Servers)"
echo "=========================================================="

# 1. Start Backend in background
echo "[1/2] Launching FastAPI Backend on http://localhost:8000..."
source backend/venv/bin/activate
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# 2. Start Frontend in background
echo "[2/2] Launching Vite React Frontend on http://localhost:5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT

echo ""
echo "✨ Healix is running!"
echo "   • Frontend: http://localhost:5173"
echo "   • Backend API Docs: http://localhost:8000/docs"
echo "   • Demo User: demo@healix.ai / HealixDemo2026!"
echo ""
echo "Press Ctrl+C to stop both servers."
wait

