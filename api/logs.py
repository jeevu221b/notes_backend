from django.http import JsonResponse
import logging
from honeybadger.contrib.logger import HoneybadgerHandler

# Logger
hb_handler = HoneybadgerHandler(
    api_key='hbp_aKpVsPH4u0EAoS681F14UtgfucQ38N0zdXby')
logger = logging.getLogger('honeybadger')
logger.addHandler(hb_handler)

# Utills
key = "SECRET_KEY"
auth_route = [
    '/api/createnotes/', '/api/getnotes/', '/api/logout/', '/api/editnotes/', '/api/deletenotes/']


def HttpError(message, code=400):
    # Error handler
    logger.error(message)
    return JsonResponse({"error": message}, status=code)


error = {
    "MISSING_REQUIRED_FIELDS": "Missing required fields",
    "JSON_REQUIRED": "Invalid or missing JSON data in the request body",
    "INVALID_INPUT": "Invalid input. Please provide valid data",
    "USER_DOESN'T_EXIST": "User doesn't exist",
    "MISSING_AUTH": "Missing Authorization header",
    "INVALD_TOKEN": "Invalid token",
    "USER_ALREADY_EXISTS": "User already exists",


}


sucess = {
    "USER_CREATED": "User created succesfully :)",
    "ALREADY_LOGGED_IN": "You're already logged in :)",
    "LOGGED_OUT": "Logout Succesful :)",
    "NOTE_EDITED": "Note updated successfully :)",
    "NOTE_DELETED": "Note deleted successfully :)"

}
