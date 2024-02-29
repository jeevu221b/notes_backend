from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, TokenSerializer, NoteSerializer
from rest_framework.response import Response
import json
from json import JSONDecodeError
from .models import User, Token, Note
import jwt
from datetime import datetime, timedelta
from .tokenStatus import is_expired
from .logs import error, sucess, HttpError
from rest_framework.decorators import api_view
import datetime
from django.views.decorators.http import require_GET, require_POST
from .tokenStatus import decodeToken, validData


key = "SECRET_KEY"
# expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=15)


@api_view(["GET"])
def apiHome(request):
    if request.method == 'GET':
        return HttpResponse("<h1>This is API Home!</h1>")
    else:
        return HttpResponse("<h1>This method is not allowed</h1>", status=405)


@api_view(["POST"])
def signup(request):
    if len(request.body) > 0:
        try:
            data = json.loads(request.body)
            serializer = UserSerializer(data=data)
            try:
                try:
                    username = data["username"]
                    if User.objects.filter(username=username).exists():
                        return JsonResponse({"error": "User with this username already exists"}, status=400)

                except:
                    pass
                if serializer.is_valid():
                    print("Inside the if")
                    serializer.save()
                    return HttpResponse("User has been succesfully created!")
                else:
                    print("Inside the else")
                    print("Invalid", serializer.errors)
                    return JsonResponse({"error": error["INVALID_INPUT"]})
            except Exception as e:
                print("punk", e)
        except JSONDecodeError:
            return JsonResponse({"error": error["JSON_REQUIRED"]})
    else:
        return JsonResponse({"error": error["MISSING_REQUIRED_FIELDS"]})


# @csrf_exempt
@api_view(["POST"])
def login(request):
    if len(request.body) > 0:
        try:
            data = json.loads(request.body)
            try:
                username = data["username"]
                password = data["password"]
            except:
                return JsonResponse({"error": "Expected fields not received"})

            queryUser = User.objects.filter(
                username=username, password=password)
            if queryUser:
                us = queryUser.first()
                serialized = UserSerializer(us)
                user = serialized.data

                # Calculate expiration time dynamically
                expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=15)

                uid = {"uid": user["id"]}
                uid["exp"] = expiration_time

                auth_token = jwt.encode(uid, key)
                insertData = Token.objects.create(token=auth_token)
                return JsonResponse({"token": auth_token})
            else:
                return HttpError({"error": error["USER_DOESN'T_EXIST"]})
        except JSONDecodeError:
            return JsonResponse({"error": error["JSON_REQUIRED"]})
    else:
        return JsonResponse({"error": error["MISSING_REQUIRED_FIELDS"]})


@csrf_exempt
def token(r):
    header = r.META.get('HTTP_PUNK')
    if header:
        queryToken = Token.objects.filter(token=header)
        if queryToken:
            t = queryToken.first()
            serialized = TokenSerializer(t)
            token = serialized.data
            if token["isActive"] and is_expired(token["token"], key):
                print("Token is valid!")
                return HttpResponse("Valid Token!, Congrats you're logged in!")
            else:
                print("Invalid Token!")
        else:
            print("Token not found!")
    else:
        print("No header", header)

    return HttpResponse("This is the token page!")


@api_view(["GET"])
def getNotes(request):
    header = request.META.get('HTTP_AUTHORIZATION')
    if header:
        uid = decodeToken(header)
        if uid is not None:
            queryNote = Note.objects.filter(uid=uid)
            serialized_notes = NoteSerializer(queryNote, many=True)
            data = serialized_notes.data
            # print(data)
            # print(json.dumps(serialized_notes.data))
            return JsonResponse({"messagae": data})


@api_view(["POST"])
def createNotes(request):
    if validData(request.body):
        header = request.META.get('HTTP_AUTHORIZATION')
        if header:
            uid = decodeToken(header)
            body = json.loads(request.body)
            note = body["note"]
            if uid is not None:
                createNote = Note.objects.create(uid=uid, note=note)
                print("createNote", createNote)
                return HttpResponse("Note created!")

        else:
            print("Invalid header")
    else:
        return HttpError(error["INVALID_INPUT"])


@api_view(["POST"])
def logout(request):
    header = request.META.get('HTTP_AUTHORIZATION')
    if header:
        # print(header)
        uid = decodeToken(header)
        if uid is not None:
            update = Token.objects.filter(token=header).update(isActive=False)
            print(update)
            return JsonResponse({"message": sucess["LOGGED_OUT"], "sucess": True})
        else:
            # console.log("jeevu")
            print("jeevu")
            return HttpError(error["INVALD_TOKEN"])

    return JsonResponse({"message": "This is the Logout Page!"}, status=200)
