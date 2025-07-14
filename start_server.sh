#!/bin/bash

PORT=8010
echo "🔍 Checking for process using port $PORT..."

PID=$(lsof -ti tcp:$PORT)

if [ -n "$PID" ]; then
  echo "⚠️ Port $PORT is in use by PID $PID. Killing it..."
  kill -9 $PID
  sleep 1
fi

echo "🚀 Starting Gunicorn on port $PORT..."
exec gunicorn myMoney.asgi:application -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:$PORT
