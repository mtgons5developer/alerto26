# config/views.py (create or update)
from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.shortcuts import redirect, render

from emergencies.models import Emergency
from providers.models import Provider
from users.models import User


def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser or user.user_type == "ADMIN"


@login_required
@user_passes_test(is_staff_or_admin)
def staff_dashboard(request):
    # User statistics
    total_users = User.objects.count()
    staff_users = User.objects.filter(is_staff=True).count()
    admin_users = User.objects.filter(is_superuser=True).count()
    online_users = User.objects.filter(is_online=True).count()

    # User type breakdown
    user_types = (
        User.objects.values("user_type").annotate(count=Count("id")).order_by("-count")
    )

    # Recent staff activity
    recent_staff = User.objects.filter(
        Q(is_staff=True) | Q(is_superuser=True)
    ).order_by("-last_login")[:10]

    # Recent user signups
    recent_signups = User.objects.all().order_by("-date_joined")[:10]

    # Emergency stats
    emergency_stats = {
        "total": Emergency.objects.count(),
        "today": Emergency.objects.filter(
            created_at__date=datetime.now().date()
        ).count(),
        "active": Emergency.objects.filter(
            status__in=["pending", "dispatched"]
        ).count(),
    }

    # Provider stats
    provider_stats = {
        "total": Provider.objects.count(),
        "verified": Provider.objects.filter(is_verified=True).count(),
        "available": Provider.objects.filter(status="AVAILABLE").count(),
    }

    context = {
        # User stats
        "total_users": total_users,
        "staff_users": staff_users,
        "admin_users": admin_users,
        "online_users": online_users,
        "user_types": list(user_types),
        # Staff lists
        "recent_staff": recent_staff,
        "recent_signups": recent_signups,
        # System stats
        "emergency_stats": emergency_stats,
        "provider_stats": provider_stats,
        # Current user info
        "current_user": request.user,
    }

    return render(request, "admin/staff_dashboard.html", context)


def home_redirect(request):
    """Redirect to dashboard if logged in, otherwise to login page"""
    if request.user.is_authenticated:
        return redirect("staff_dashboard")
    else:
        return redirect("login")
