#!/bin/bash
echo "📊 AlertO24 Development Status"
echo "=============================="

# Docker services
echo ""
echo "🐳 Docker Services:"
docker-compose -f docker-compose.dev.yml ps

# Backend
echo ""
echo "🐍 Backend:"
if [ -f /tmp/alerto24-django.pid ]; then
    DJANGO_PID=$(cat /tmp/alerto24-django.pid)
    if ps -p $DJANGO_PID > /dev/null; then
        echo "✅ Django running (PID: $DJANGO_PID)"
        echo "   API: http://localhost:8000"
        echo "   GraphQL: http://localhost:8000/graphql"
        echo "   Admin: http://localhost:8000/admin"
    else
        echo "❌ Django not running"
    fi
else
    echo "❌ Django not running"
fi

# Frontend
echo ""
echo "⚛️ Frontend:"
if [ -f /tmp/alerto24-react.pid ]; then
    REACT_PID=$(cat /tmp/alerto24-react.pid)
    if ps -p $REACT_PID > /dev/null; then
        echo "✅ React running (PID: $REACT_PID)"
        echo "   Dashboard: http://localhost:3000"
    else
        echo "❌ React not running"
    fi
else
    echo "❌ React not running"
fi

# Database
echo ""
echo "🗄️ Database:"
if docker-compose -f docker-compose.dev.yml ps postgres | grep -q "Up"; then
    echo "✅ PostgreSQL running"
    echo "   Host: localhost:5432"
    echo "   Database: alerto24_dev"
else
    echo "❌ PostgreSQL not running"
fi

# Redis
echo ""
echo "🔴 Redis:"
if docker-compose -f docker-compose.dev.yml ps redis | grep -q "Up"; then
    echo "✅ Redis running"
    echo "   Host: localhost:6379"
else
    echo "❌ Redis not running"
fi
