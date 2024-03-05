from .logs import error, HttpError, sucess, key
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
import jwt
from jwt import ExpiredSignatureError
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from .models import Token
from .serializers import TokenSerializer
import json
from json import JSONDecodeError


def is_expired(token, key):
    try:
        data = jwt.decode(token, key, algorithms="HS256")
        return data["uid"]

    except ExpiredSignatureError:
        return None

    except InvalidSignatureError:
        return HttpResponse("Invalid Singature error")


def decodeToken(header):
    queryToken = Token.objects.filter(token=header)
    if queryToken:
        t = queryToken.first()
        serialized = TokenSerializer(t)
        token = serialized.data
        uid = is_expired(token["token"], key)
        if token["isActive"] and uid is not None:
            return uid
        else:
            return None
    else:
        return None


def validData(data):
    if len(data) > 0:
        try:
            data = json.loads(data)
            note = data["note"]
            return True

        except:
            return False
    else:
        return False


def validToken(header, key):
    queryToken = Token.objects.filter(token=header)
    if queryToken:
        t = queryToken.first()
        serialized = TokenSerializer(t)
        token = serialized.data
        uid = is_expired(token["token"], key)
        if token["isActive"] and uid is not None:
            return sucess["ALREADY_LOGGED_IN"]
        else:
            return error["INVALD_TOKEN"]
    else:
        return error["INVALD_TOKEN"]
