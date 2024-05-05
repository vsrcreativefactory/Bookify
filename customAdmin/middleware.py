# customAdmin/middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class AdminAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        admin_paths = ['/dashboard/', '/admin_home/', '/adminprofile/',  # Add all your admin paths here
                       '/all_products/', '/add_products/', '/edit_products/',
                       '/manage_products/', '/delete_product/', '/all_users/',
                       '/add_users/', '/edit_users/', '/manage_users/',
                       '/delete_user/', '/block_user/', '/unblock_user/',
                       '/all_categories/', '/add_categories/', '/edit_categories/',
                       '/delete_category/']
        
        # Check if request path is in admin_paths and user is not authenticated
        if request.path in admin_paths and not request.user.is_authenticated:
            return redirect('/admin/')  # Redirect to admin login page

        # For paths not in admin_paths, or if user is authenticated, no action is needed
