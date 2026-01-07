#!/bin/bash
set -e

echo "🚀 Starting AlertO24 Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for required commands
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        exit 1
    fi
}

echo "🔍 Checking prerequisites..."
check_command docker
check_command docker-compose
check_command python3
check_command node
check_command flutter

# Start infrastructure
echo "🐳 Starting Docker services..."
docker-compose -f docker-compose.dev.yml up -d postgres redis

# Wait for databases to be ready
echo "⏳ Waiting for databases..."
sleep 5

# Backend setup
echo "🐍 Setting up Python backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found in backend/ ${NC}"
    echo "Creating from example..."
    cp ../.env.example .env
fi

# Run migrations
echo "📦 Running database migrations..."
python manage.py migrate

# Create superuser if not exists
echo "👑 Creating admin user..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@alerto24.app', 'admin123')
    print("Admin user created: admin / admin123")
else:
    print("Admin user already exists")
END

# Start Django dev server in background
echo "🚀 Starting Django server..."
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!
cd ..

# Frontend setup
echo "⚛️ Setting up React admin..."
cd admin-dashboard
if [ ! -d "node_modules" ]; then
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating frontend .env..."
    echo "VITE_API_URL=http://localhost:8000" > .env
    echo "VITE_WS_URL=ws://localhost:8000/ws" >> .env
fi

# Start React dev server in background
echo "🚀 Starting React dev server..."
npm start &
REACT_PID=$!
cd ..

# Mobile setup
echo "📱 Setting up Flutter mobile..."
cd mobile_app
flutter pub get

echo ""
echo -e "${GREEN}✅ Development environment started!${NC}"
echo ""
echo "🌐 Access URLs:"
echo "   Backend API:    http://localhost:8000"
echo "   GraphQL:        http://localhost:8000/graphql"
echo "   Admin Dashboard: http://localhost:3000"
echo "   Django Admin:   http://localhost:8000/admin (admin/admin123)"
echo ""
echo "📱 Mobile App:"
echo "   cd mobile_app && flutter run"
echo ""
echo "🛑 To stop all services:"
echo "   ./scripts/dev-stop.sh"
echo ""
echo "📊 To check service status:"
echo "   ./scripts/dev-status.sh"

# Save PIDs to file
echo "$DJANGO_PID" > /tmp/alerto24-django.pid
echo "$REACT_PID" > /tmp/alerto24-react.pid

# Wait for user interrupt
trap 'echo "Shutting down..."; kill $DJANGO_PID $REACT_PID; exit 0' INT
wait
