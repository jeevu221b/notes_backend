# refactor the code below
from django.http import JsonResponse

error = {
    "MISSING_REQUIRED_FIELDS": "Missing required fields",
    "JSON_REQUIRED": "Invalid or missing JSON data in the request body",
    "INVALID_INPUT": "Invalid input. Please provide valid data",
    "USER_DOESN'T_EXIST": "User doesn't exist",
    "MISSING_AUTH": "Missing Authorization header",
    "INVALD_TOKEN": "Invalid token",
}


def HttpError(message, code=400):
    return JsonResponse({"error": message}, status=code)


sucess = {
    "USER_CREATED": "User created succesfully!",
    "ALREADY_LOGGED_IN": "You're already logged in :)",
    "LOGGED_OUT": "Logout Succesful :)"
}
