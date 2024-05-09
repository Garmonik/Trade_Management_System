from datetime import datetime, timedelta

import jwt

from shop_statistic import settings


def get_token(user):
    access_payload = {
        'access_key': str(user.access_key),
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(seconds=3600)
    }
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')

    refresh_payload = {
        'access_key': str(user.access_key),
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(seconds=3600*24*30)
    }
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    return access_token, refresh_token
