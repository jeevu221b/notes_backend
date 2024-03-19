from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, TokenSerializer, NoteSerializer
import json
from json import JSONDecodeError
from .models import User, Token, Note
import jwt
from datetime import datetime, timedelta
from .tokenStatus import is_expired, decodeToken, validData
from .logs import error, sucess, HttpError, key
from rest_framework.decorators import api_view
import datetime
from .recommender import get_recommendation


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
                username = data["username"]
                if User.objects.filter(username=username).exists():
                    return HttpError(error["USER_ALREADY_EXISTS"])

            except:
                pass
            if serializer.is_valid():
                print("Inside the if")
                serializer.save()
                return HttpError(sucess["USER_CREATED"], 201)
            else:
                return HttpError(error["INVALID_INPUT"])

        except JSONDecodeError:
            return HttpError(error["JSON_REQUIRED"])
    else:
        return HttpError(error["MISSING_REQUIRED_FIELDS"])


@api_view(["POST"])
def login(request):
    if len(request.body) > 0:
        try:
            data = json.loads(request.body)
            try:
                username = data["username"]
                password = data["password"]
            except:
                return HttpError(error["MISSING_REQUIRED_FIELDS"])

            queryUser = User.objects.filter(
                username=username, password=password)
            if queryUser:
                us = queryUser.first()
                serialized = UserSerializer(us)
                user = serialized.data
                expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=15)
                uid = {"uid": user["id"]}
                uid["exp"] = expiration_time
                auth_token = jwt.encode(uid, key)
                insertData = Token.objects.create(token=auth_token)
                return JsonResponse({"token": auth_token})
            else:
                return HttpError(error["USER_DOESN'T_EXIST"])
        except JSONDecodeError:
            return HttpError(error["JSON_REQUIRED"])
    else:
        return HttpError(error["MISSING_REQUIRED_FIELDS"])


@api_view(["POST"])
def logout(request):
    header = request.META.get('HTTP_AUTHORIZATION')
    if header:
        uid = decodeToken(header)
        if uid is not None:
            update = Token.objects.filter(token=header).update(isActive=False)
            return JsonResponse({"message": sucess["LOGGED_OUT"], "sucess": True})
        else:

            return HttpError(error["INVALD_TOKEN"])


@api_view(["GET"])
def getNotes(request, id=None):
    header = request.META.get('HTTP_AUTHORIZATION')
    if header:
        uid = decodeToken(header)
        if id is None:
            if uid is not None:
                queryNote = Note.objects.filter(uid=uid)
                serialized_notes = NoteSerializer(queryNote, many=True)
                data = serialized_notes.data
                return JsonResponse({"message": data})
            else:
                return HttpError(error["INVALD_TOKEN"])
        else:
            try:
                queryNote = Note.objects.filter(note_id=int(id))
                if queryNote:
                    serialized_notes = NoteSerializer(queryNote, many=True)
                    data = serialized_notes.data
                    return JsonResponse({"message": data[0]})
                else:
                    return HttpError("Note not found")
            except:
                return HttpError(error["INVALID_INPUT"])


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
                return JsonResponse({"message": "Note created!"}, status=201)

        else:
            return HttpError(error["INVALD_TOKEN"])
    else:
        return HttpError(error["INVALID_INPUT"])


@api_view(["POST"])
def editNotes(request):
    if (request.body):
        header = request.META.get('HTTP_AUTHORIZATION')
        if header:
            uid = decodeToken(header)
            body = json.loads(request.body)
            try:
                note_id = body["note_id"]
                note = body["note"]
            except:
                return HttpError(error["INVALID_INPUT"])
            if uid is not None:
                editNote = Note.objects.filter(
                    uid=uid, note_id=note_id).first()
                if editNote:
                    print("Inside the EDIT NOTE")
                    editNote.note = body["note"]
                    editNote.save()
                    return JsonResponse({"message": sucess["NOTE_EDITED"]}, status=200)
                else:
                    return HttpError(error["USER_DOESN'T_EXIST"])

        else:
            return HttpError(error["INVALD_TOKEN"])

    else:
        return HttpError(error["INVALID_INPUT"])


@api_view(["POST"])
def deleteNotes(request):
    if (request.body):
        header = request.META.get('HTTP_AUTHORIZATION')
        if header:
            uid = decodeToken(header)

            body = json.loads(request.body)
            try:
                note_id = body["note_id"]
            except:
                return HttpError(error["INVALID_INPUT"])
            if uid is not None:
                deletNote = Note.objects.filter(
                    uid=uid, note_id=note_id).first()
                if deletNote:
                    deletNote.delete()
                    return JsonResponse({"message": sucess["NOTE_DELETED"]}, status=200)
                else:
                    return HttpError(error["USER_DOESN'T_EXIST"])
            else:
                return HttpError(error["INVALD_TOKEN"])
    else:
        return HttpError(error["INVALID_INPUT"])


@api_view(["POST"])
def getRecommendation(request):
    try:
        movie = json.loads(request.body)
        recommendation = get_recommendation(movie["movie"])
    except:
        return JsonResponse({"message": "Enter Valid Data"}, status=401)
    if recommendation != "":
        return JsonResponse({"recommendations": recommendation}, status=201)
    else:
        return JsonResponse({"message": "Movie not in the DB"}, status=401)
    # return HttpResponse("This is the recommendation Page")
