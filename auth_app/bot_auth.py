from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from .models import Bot

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the token from the request headers
        token = request.headers.get('Authorization')
        if not token:
            return None
        
        # Try to retrieve the bot associated with the token
        try:
            bot_token = Bot.objects.get(bot_father_token=token)
            user = User.objects.first()
        except Bot.DoesNotExist:
            raise AuthenticationFailed('Invalid or expired token')
        
        # Return an anonymous user-like object and the bot token instance
        return (user, bot_token)