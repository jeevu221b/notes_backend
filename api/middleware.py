
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
        from .logs import error, HttpError, key, auth_route

        url = request.path
        if url in auth_route or url.startswith('/api/getnotes/'):
            header = request.META.get('HTTP_AUTHORIZATION')
            if header:
                res = validToken(header, key)
            else:
                return HttpError(error["MISSING_AUTH"])

        else:
            print("Not among the specified route!")
            header = request.META.get('HTTP_AUTHORIZATION')
            if header:
                res = validToken(header, key)
                return HttpResponse(res)

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
