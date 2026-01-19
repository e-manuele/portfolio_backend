import jwt
import os
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from decouple import config

JWT_SECRET = config('JWT_SECRET', default='your-secret-key')
JWT_ALGORITHM = config('JWT_ALGORITHM', default='HS256')
JWT_EXPIRATION_HOURS = config('JWT_EXPIRATION_HOURS', default=24, cast=int)


def generate_jwt_token(user):
    """Genera un token JWT per l'utente"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt_token(token):
    """Verifica e decodifica un token JWT"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token scaduto')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Token non valido')


class JWTAuthentication(TokenAuthentication):
    """Autenticazione personalizzata con JWT"""
    keyword = 'Bearer'
    
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()
        
        if not auth or auth[0].lower() != self.keyword.lower():
            return None
        
        if len(auth) == 1:
            raise AuthenticationFailed('Token mancante')
        
        if len(auth) > 2:
            raise AuthenticationFailed('Token non valido')
        
        token = auth[1]
        
        try:
            payload = verify_jwt_token(token)
            user = User.objects.get(id=payload['user_id'])
            return (user, token)
        except User.DoesNotExist:
            raise AuthenticationFailed('Utente non trovato')
        except AuthenticationFailed:
            raise
