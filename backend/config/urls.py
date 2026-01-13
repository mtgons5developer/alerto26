# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.http import HttpResponse
from . import views
from .schema import schema
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.shortcuts import redirect
import debug_toolbar
from providers.views import test_debug


# Home redirect view
def home_redirect(request):
    """Redirect to dashboard if logged in, otherwise to login"""
    if request.user.is_authenticated:
        return redirect('staff_dashboard')
    else:
        return redirect('login')

# Protect admin with custom login (optional - can remove if causing issues)
# admin.site.login = login_required(admin.site.login)

urlpatterns = [
    # Home page redirect
    path('', home_redirect, name='home'),
    
    # Admin URLs
    path('admin/', admin.site.urls),
    
    # Custom login/logout (using /accounts/ to match settings.py)
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='admin/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='login'  # Use name instead of hardcoded URL
    ), name='logout'),
    
    # Dashboard (protected)
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # GraphQL API
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    
    # Health check
    path('health/', lambda request: HttpResponse('OK')),
    
    # Keep old /login/ for compatibility (redirects to /accounts/login/)
    path('login/', lambda request: redirect('login')),

    path("__debug__/", include(debug_toolbar.urls)),
    path("debug-test/", test_debug),
]