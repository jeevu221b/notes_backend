
class TestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        from django.http import HttpResponse, JsonResponse
        from .models import Token
        from .serializers import TokenSerializer
        from .tokenStatus import is_expired, validToken
        from django.shortcuts import redirect
        from .logs import error, HttpError

        key = "SECRET_KEY"

        auth_route = [
            '/api/createNotes/', '/api/getNotes/', '/api/logout/']
        url = request.path
        if url in auth_route:
            header = request.META.get('HTTP_AUTHORIZATION')
            if header:
                res = validToken(header, key)
                # print("You're already logged in!")

                # return HttpResponse(res)
                # queryToken = Token.objects.filter(token=header)
                # if queryToken:
                #     t = queryToken.first()
                #     serialized = TokenSerializer(t)
                #     token = serialized.data
                #     # print("Punkstar", token)
                #     uid = is_expired(token["token"], key)
                #     if token["isActive"] and uid is not None:
                #         print("Token is valid")
                #     else:
                #         return HttpError(error["INVALD_TOKEN"])
                # else:
                #     return HttpError(error["INVALD_TOKEN"])

            else:
                return HttpError(error["MISSING_AUTH"])

        else:
            print("Not among the specified route!")
            print("Before response")
            header = request.META.get('HTTP_AUTHORIZATION')
            if header:
                res = validToken(header, key)
                # print("You're already logged in!")
                return HttpResponse(res)
            # else:
            #     return HttpError(error["MISSING_AUTH"])

        response = self.get_response(request)
        # print("After response")
        # Code to be executed for each request/response after
        # the view is called.

        return response
