@echo off
echo Starting Intelligent Innovation Copilot...

REM =========================
REM 1. Setup Python venv
REM =========================
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate

echo Installing backend dependencies...
pip install --upgrade pip
pip install -r backend\requirements.txt
pip install aiosqlite beautifulsoup4 cachetools psycopg[binary]

REM =========================
REM 2. Set environment vars
REM =========================
set PATENT_SOURCE=lens
set PATENT_SOURCE_FALLBACK=none

set LENS_API_TOKEN=YOUR_LENS_API_KEY
set LENS_API_URL=https://api.lens.org/patent/search

set DATABASE_URL=sqlite+aiosqlite:///./test.db

set MCP_RETRIEVAL_URL=http://127.0.0.1:8101
set MCP_EVIDENCE_URL=http://127.0.0.1:8103
set MCP_NOVELTY_URL=http://127.0.0.1:8104
set MCP_REPORT_URL=http://127.0.0.1:8106

set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:9000/api/v1

REM =========================
REM 3. Start backend services
REM =========================
echo Starting MCP services...

start cmd /k "uvicorn backend.mcp_servers.retrieval.server:app --port 8101"
start cmd /k "uvicorn backend.mcp_servers.evidence.server:app --port 8103"
start cmd /k "uvicorn backend.mcp_servers.novelty.server:app --port 8104"
start cmd /k "uvicorn backend.mcp_servers.report.server:app --port 8106"

timeout /t 5

echo Starting main backend...
start cmd /k "uvicorn backend.app.main:app --port 9000"

REM =========================
REM 4. Start frontend
REM =========================
echo Installing frontend dependencies...
cd frontend
call npm install

echo Starting frontend...
start cmd /k "npx next dev -H 127.0.0.1 -p 5006"

cd ..

echo ====================================
echo App is starting...
echo Open: http://127.0.0.1:5006/idea-input
echo ====================================
pause