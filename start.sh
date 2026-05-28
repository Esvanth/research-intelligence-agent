#!/bin/bash
# start.sh — Starts both FastAPI backend and React frontend

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🧠 Research Intelligence Agent"
echo "  Agents League Hackathon 2026 | Foundry IQ"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check .env exists
if [ ! -f .env ]; then
  echo "❌ ERROR: .env file not found!"
  echo ""
  echo "   Run this first:"
  echo "   cp .env.example .env"
  echo "   Then open .env and fill in your Azure credentials."
  echo ""
  exit 1
fi

# Check virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
  echo "⚠️  Virtual environment not active."
  echo "   Run: source .venv/bin/activate"
  echo "   Then run this script again."
  echo ""
  exit 1
fi

# Check frontend dependencies
if [ ! -d "frontend/node_modules" ]; then
  echo "📦 Installing frontend dependencies..."
  cd frontend && npm install && cd ..
fi

# Start FastAPI backend in background
echo "▶ Starting FastAPI backend → http://localhost:8000"
python app.py &
BACKEND_PID=$!

# Give backend 2 seconds to start
sleep 2

# Check backend started
if ! kill -0 $BACKEND_PID 2>/dev/null; then
  echo "❌ Backend failed to start. Check your .env credentials."
  exit 1
fi

echo "▶ Starting React frontend → http://localhost:5173"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Open browser at: http://localhost:5173"
echo "  Press Ctrl+C to stop both servers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start frontend (blocking)
cd frontend && npm run dev

# When frontend stops, kill backend
kill $BACKEND_PID 2>/dev/null
echo "Servers stopped."
