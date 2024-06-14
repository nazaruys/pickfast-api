from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError


def is_valid_password(password):
            if type(password) != str:
                return False
            if len(password) < 8:
                return False
            if not any(char.isupper() for char in password):
                return False
            if not any(char.islower() for char in password):
                return False
            if not any(char.isdigit() for char in password):
                return False
            return True

def is_refresh_token_blacklisted(token):
    try:
        token_obj = RefreshToken(token)
        return BlacklistedToken.objects.filter(token__jti=token_obj['jti']).exists()
    except TokenError as e:
        if 'blacklisted' in str(e):
            return True
        return False
    