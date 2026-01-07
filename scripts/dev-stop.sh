#!/bin/bash
echo "🛑 Stopping AlertO24 development services..."

# Stop background processes
if [ -f /tmp/alerto24-django.pid ]; then
    DJANGO_PID=$(cat /tmp/alerto24-django.pid)
    kill $DJANGO_PID 2>/dev/null && echo "Stopped Django server"
    rm /tmp/alerto24-django.pid
fi

if [ -f /tmp/alerto24-react.pid ]; then
    REACT_PID=$(cat /tmp/alerto24-react.pid)
    kill $REACT_PID 2>/dev/null && echo "Stopped React server"
    rm /tmp/alerto24-react.pid
fi

# Stop Docker services
docker-compose -f docker-compose.dev.yml down

echo "✅ All services stopped"
