import jwt
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect

from sports_booking import settings


def check_jwt(request: WSGIRequest | str, content):
    if type(request) == str:
        raw_token = request
    else:
        raw_token = request.COOKIES.get('access_token')
    if raw_token is None:
        return redirect('/admin/login')
    try:
        decoded = jwt.decode(raw_token, settings.SECRET_KEY, algorithms=['HS256'])
        return content
    except jwt.ExpiredSignatureError:
        print("Token is expired")
        return redirect('/admin/login')
    except jwt.InvalidTokenError:
        print("Invalid token")
        return redirect('/admin/login')