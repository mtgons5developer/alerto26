#!/bin/bash
echo "🔍 Checking Django setup..."

# Check if in backend directory
if [[ ! $(pwd) =~ "backend" ]]; then
    echo "❌ Not in backend directory"
    echo "Run: cd backend"
    exit 1
fi

# Check virtual environment
if [[ ! $VIRTUAL_ENV ]]; then
    echo "❌ Virtual environment not activated"
    echo "Run: source venv/bin/activate"
    exit 1
else
    echo "✅ Virtual environment: $VIRTUAL_ENV"
fi

# Check Python
echo "Python: $(python --version)"
echo "Pip: $(pip --version | head -1)"

# Check Django
if python -c "import django" 2>/dev/null; then
    echo "✅ Django installed: $(python -c "import django; print(django.__version__)")"
else
    echo "❌ Django not installed"
    echo "Run: pip install django"
fi

# Check manage.py
if [ -f "manage.py" ]; then
    echo "✅ manage.py exists"
    python manage.py check --deploy --fail-level WARNING 2>/dev/null && echo "✅ Django checks pass"
else
    echo "❌ manage.py missing"
fi
