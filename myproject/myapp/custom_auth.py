# custom_auth.py

from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model

class WebsiteSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        # Call the authenticate method of the parent class
        user_auth_tuple = super().authenticate(request)
        
        # If user is not authenticated through session, return None
        if user_auth_tuple is None:
            return None
        
        # Extract user and auth tuple
        user, _ = user_auth_tuple
        
        # Here, you might want to add logic to check if the user is already authenticated in Django Rest Framework
        # This could involve checking a flag or setting a custom attribute on the user object
        
        # Return user and authentication tuple
        return user, None
