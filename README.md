```markdown
# 🚨 Alerto24 - Emergency Response Platform

A real-time emergency response and alert system built with Django, GraphQL, and PostgreSQL. Connects citizens with emergency services through a modern API-first architecture.

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![GraphQL](https://img.shields.io/badge/GraphQL-E10098.svg)](https://graphql.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.1-blue.svg)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Database Models](#-database-models)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🚨 Emergency Management
- Real-time emergency reporting with geolocation
- Multiple emergency types: Medical, Fire, Police, Accidents, Natural Disasters
- Priority levels (Low → Medium → High → Critical)
- Anonymous reporting support
- Multimedia attachments (photos, documents)
- Patient medical information storage

### 👥 User System
- Multi-type user roles: Citizen, Provider, First Responder, Admin
- Emergency contacts and medical profiles
- Location tracking and status indicators
- Push notification preferences
- Blood type and medical condition storage

### 🏥 Provider Network
- Verified emergency service providers
- Service type classification (Ambulance, Fire Truck, Police, etc.)
- Real-time availability status
- Performance metrics and ratings
- Geographic service coverage
- Scheduling and capacity management

### 🔧 Technical Features
- Modern GraphQL API with real-time capabilities
- JWT authentication and authorization
- PostgreSQL with JSON field support
- Comprehensive error handling
- Health monitoring endpoints
- Docker containerization
- Extensive testing suite

## 🛠 Tech Stack

### Backend
- **Framework**: Django 4.2+
- **API**: GraphQL (graphene-django)
- **Authentication**: JWT (graphql-jwt)
- **Database**: PostgreSQL 18.1
- **Task Queue**: Celery (planned)
- **Real-time**: WebSockets (planned)

### Frontend (Future)
- **Mobile**: React Native / Flutter
- **Web Dashboard**: React.js / Next.js
- **Maps**: Mapbox / Google Maps API

### DevOps
- **Container**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana (planned)

## 🏗 Architecture

```
Alerto24 Architecture
├── API Layer (GraphQL)
│   ├── Queries (Read operations)
│   ├── Mutations (Write operations)
│   └── Subscriptions (Real-time updates - planned)
├── Business Logic
│   ├── Emergency Dispatch System
│   ├── Provider Matching Algorithm
│   ├── Notification Service
│   └── Location Services
├── Data Layer
│   ├── PostgreSQL Database
│   ├── Redis Cache (planned)
│   └── File Storage (S3/MinIO)
└── Client Applications
    ├── Citizen Mobile App
    ├── Provider Mobile App
    └── Admin Web Dashboard
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 14+ (or Docker)
- Node.js 16+ (for frontend development)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/alerto24.git
cd alerto24/backend
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=alerto24
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 4. Set Up Database

#### Option A: Using Docker (Recommended)
```bash
# Start PostgreSQL container
docker run --name alerto24-postgres \
  -e POSTGRES_DB=alerto24 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=123456 \
  -p 5432:5432 \
  -d postgres:latest

# Verify it's running
docker ps | grep postgres
```

#### Option B: Local PostgreSQL
```bash
# Create database
createdb alerto24

# Or via psql
psql -U postgres -c "CREATE DATABASE alerto24;"
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Generate Test Data
```bash
# Create realistic test data
python scripts/testing/create_alerto_test_data.py
```

### 8. Start Development Server
```bash
python manage.py runserver
```

Visit:
- **API Explorer**: http://localhost:8000/graphql/
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/health/

## 📚 API Documentation

### GraphQL Endpoint
```
POST http://localhost:8000/graphql/
```

### Authentication
```graphql
# Get JWT token
mutation {
  tokenAuth(username: "admin", password: "admin123") {
    token
    refreshToken
    user {
      id
      username
      email
    }
  }
}

# Use token in headers
Authorization: JWT <your_token_here>
```

### Sample Queries

#### List Emergencies
```graphql
query {
  emergencies {
    id
    code
    emergencyType
    priority
    status
    city
    latitude
    longitude
    isAnonymous
    createdAt
    user {
      firstName
      lastName
      phone
    }
  }
}
```

#### List Available Providers
```graphql
query {
  providers(status: "AVAILABLE") {
    id
    user {
      firstName
      lastName
      email
    }
    serviceTypes
    status
    latitude
    longitude
    rating
    vehicleType
    vehicleCapacity
    maxDistance
  }
}
```

#### Create New Emergency
```graphql
mutation {
  createEmergency(
    emergencyType: "medical"
    latitude: 14.5995
    longitude: 120.9842
    priority: "high"
    description: "Chest pain and difficulty breathing"
    city: "Manila"
  ) {
    emergency {
      id
      code
      emergencyType
      priority
      status
      latitude
      longitude
      createdAt
    }
  }
}
```

#### Get Emergency Statistics
```graphql
query {
  emergencyStats {
    total
    byType {
      type
      count
    }
    byStatus {
      status
      count
    }
    byCity {
      city
      count
    }
  }
}
```

## 🗄 Database Models

### User Model
```python
class User(AbstractUser):
    # Custom fields
    phone = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(max_length=20)  # CITIZEN, PROVIDER, ADMIN
    emergency_contacts = models.JSONField()
    medical_info = models.JSONField()
    blood_type = models.CharField(max_length=5)
    last_known_location = models.CharField(max_length=100)
    is_online = models.BooleanField(default=False)
```

### Emergency Model
```python
class Emergency(models.Model):
    code = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    provider = models.ForeignKey(Provider, null=True, on_delete=models.SET_NULL)
    emergency_type = models.CharField(max_length=50)  # medical, fire, police
    priority = models.CharField(max_length=20)  # low, medium, high, critical
    status = models.CharField(max_length=20)  # pending, dispatched, arrived, resolved
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    symptoms = models.JSONField()
    patient_info = models.JSONField()
    attachments = models.JSONField()
    is_anonymous = models.BooleanField(default=False)
```

### Provider Model
```python
class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_types = models.JSONField()  # [AMBULANCE, FIRE_TRUCK, POLICE_CAR]
    status = models.CharField(max_length=20)  # AVAILABLE, ON_DUTY, IN_EMERGENCY
    latitude = models.FloatField()
    longitude = models.FloatField()
    certification_level = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    total_emergencies = models.IntegerField(default=0)
    completed_emergencies = models.IntegerField(default=0)
    vehicle_type = models.CharField(max_length=50)
    vehicle_capacity = models.IntegerField(default=1)
```

## 💻 Development

### Project Structure
```
alerto24/
├── backend/                    # Django backend
│   ├── config/                # Project configuration
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py           # URL routing
│   │   └── schema.py         # GraphQL schema
│   ├── emergencies/          # Emergency management app
│   ├── providers/            # Provider management app
│   ├── users/               # Custom user management
│   ├── scripts/             # Utility scripts
│   └── manage.py
├── frontend/                 # React frontend (planned)
├── docker-compose.yml       # Multi-container setup
├── Dockerfile              # Backend container
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test emergencies

# Run with coverage
coverage run manage.py test
coverage report
```

### Code Quality
```bash
# Run linter
flake8 .

# Check imports
isort --check-only .

# Type checking
mypy .
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations

# Create database backup
python manage.py dumpdata --indent 2 > backup.json

# Load database backup
python manage.py loaddata backup.json
```

## 🧪 Testing

### Test Data Generation
```bash
# Generate comprehensive test data
python scripts/testing/create_alerto_test_data.py

# Generate minimal test data
python scripts/testing/create_minimal_data.py

# Clear test data
python scripts/testing/clear_test_data.py
```

### GraphQL Testing
```bash
# Test GraphQL endpoints
python scripts/testing/test_graphql_endpoints.py

# Test authentication
python scripts/testing/test_auth.py

# Load test with k6 (planned)
k6 run scripts/load_tests/emergency_report.js
```

### API Testing Examples
```bash
# Test emergency creation
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createEmergency(emergencyType: \"medical\", latitude: 14.5, longitude: 121.0) { emergency { code } } }"}'

# Test provider query
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ providers { user { firstName } serviceTypes status } }"}'
```

## 🚢 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up HTTPS with SSL certificates
- [ ] Configure production database (AWS RDS, etc.)
- [ ] Set up monitoring (Prometheus, Grafana)
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Configure error tracking (Sentry)
- [ ] Set up logging aggregation

### Environment Variables (Production)
```env
# Required
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgres://user:password@host:port/database
ALLOWED_HOSTS=alerto24.com,api.alerto24.com

# Optional but recommended
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
SENTRY_DSN=your-sentry-dsn
```

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python manage.py test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Use descriptive variable names
- Write docstrings for functions and classes
- Add type hints where applicable
- Write tests for new features
- Update documentation for API changes

### Branch Naming Convention
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical production fixes
- `release/` - Release preparation
- `docs/` - Documentation updates

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the excellent web framework
- GraphQL community for the flexible API specification
- PostgreSQL team for the robust database system
- All contributors who help improve Alerto24

## 📞 Support

For support, please:
1. Check the [documentation](https://docs.alerto24.com)
2. Search existing [issues](https://github.com/yourusername/alerto24/issues)
3. Create a new issue with detailed information

## 🔗 Links

- **Website**: https://alerto24.com
- **API Documentation**: https://docs.alerto24.com/api
- **Issue Tracker**: https://github.com/yourusername/alerto24/issues
- **Changelog**: https://github.com/yourusername/alerto24/releases

---

<div align="center">
  Made with ❤️ for safer communities
</div>
```

This comprehensive README includes:
1. **Project overview** with badges
2. **Detailed features** of the emergency response system
3. **Complete tech stack** information
4. **Quick start guide** with step-by-step instructions
5. **API documentation** with GraphQL examples
6. **Database model** explanations
7. **Development guidelines** and project structure
8. **Testing instructions** with scripts
9. **Deployment checklist** for production
10. **Contributing guidelines** and coding standards
11. **License information** and acknowledgments
