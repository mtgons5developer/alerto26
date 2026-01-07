# backend/config/middleware.py
class AppendSlashMiddleware:
    """Middleware to handle trailing slashes for POST requests"""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # For GraphQL POST requests without slash, redirect with data preservation
        if request.method == 'POST' and request.path == '/graphql':
            from django.http import HttpResponseRedirect
            from django.utils.http import urlencode
            import json
            
            # Get POST data
            body = request.body.decode('utf-8')
            # Create redirect with data
            response = HttpResponseRedirect('/graphql/')
            # Store data in session or custom header for recreation
            request.META['HTTP_X_ORIGINAL_BODY'] = body
            return response
        
        return self.get_response(request)

# Add to MIDDLEWARE in settings.py:
# MIDDLEWARE = [
#     ...
#     'config.middleware.AppendSlashMiddleware',
# ]