import asyncio
from datetime import datetime, timedelta

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import sync_and_async_middleware

from product.models import Admin
from shop_statistic import settings
import jwt


def get_user(request):
    try:
        if 'access_token' in request.COOKIES:
            token = request.COOKIES['access_token']
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            email = payload.get('email')
            access_key = payload.get('access_key')
            user = Admin.objects.filter(email=email, access_key=access_key)
            if payload and user.exists():
                user = user.first()
                return user
    except:
        return None
    return None


def universal_middleware(func):

    @sync_and_async_middleware
    def wrapper(get_response):
        u_middleware = func(get_response)
        if asyncio.iscoroutinefunction(get_response):
            async def middleware(request):
                return await u_middleware(request)
        else:
            middleware = u_middleware
        return middleware
    return wrapper


def is_active_token(token):
    if token == "" or token is None:
        return False
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        expiration_time = payload.get('exp')
        expiration_datetime = datetime.fromtimestamp(expiration_time)
        current_time = datetime.utcnow()

        if current_time < expiration_datetime:
            return True
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.DecodeError:
        return False


def get_access_token(refresh_token):
    try:
        refresh_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        access_key = refresh_payload.get('access_key')
        email = refresh_payload.get('email')

        if access_key is None:
            return None

        access_payload = {
            'access_key': access_key,
            'email': email,
            'exp': datetime.utcnow() + timedelta(seconds=3600)
        }
        refresh_payload = {
            'access_key': access_key,
            'email': email,
            'exp': datetime.utcnow() + timedelta(seconds=3600*24*30)
        }
        access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
        new_refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

        return access_token, new_refresh_token
    except jwt.ExpiredSignatureError:
        return None, None
    except jwt.DecodeError:
        return None, None


@universal_middleware
class CheckTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        paths_that_dont_need_check = [
            reverse('login'),
            reverse('register'),
        ]
        if request.path not in paths_that_dont_need_check:
            if 'access_token' not in request.COOKIES and not is_active_token(request.COOKIES.get('access_token')):
                try:
                    new_tokens, new_refresh_token = get_access_token(request.COOKIES.get('refresh_token'))
                except:
                    new_tokens = None
                    new_refresh_token = None
                if new_tokens is not None:
                    request.COOKIES['access_token'] = new_tokens
                    request.COOKIES['refresh_token'] = new_refresh_token
                    response = self.get_response(request)
                    response.set_cookie('access_token', new_tokens, httponly=True)
                    response.set_cookie('refresh_token', new_refresh_token, httponly=True)
                    return response
                else: return redirect('/login/')
        response = self.get_response(request)
        return response


@universal_middleware
def GetUserMiddleware(get_response):
    def middleware(request):
        if user := get_user(request):
            request.user = request._user = user
        return get_response(request)
    return middleware
