from urllib.parse import urlencode

from app.utils import httpcodes

class UIException(Exception):
    def __init__(self, user_msg="An error occured", route_name=None, route_args=[], query_params=None):
        self.user_msg = user_msg
        self.route_name = route_name
        self.route_args = route_args

        if self.route_name is not None:
            if not query_params:
                self.query_params = ''
            elif isinstance(query_params, str):
                self.query_params = "?" + query_params
            elif isinstance(query_params, dict):
                self.query_params = "?" + urlencode(query_params)
            else:
                # TODO: error out
                self.query_params = ''

class HttpException(Exception):
    def __init__(self, msg, code, data=None):
        self.code = code
        self.msg = msg
        self.data = data

# Common exceptions
class HttpExceptionBadRequest(HttpException):
    def __init__(self):
        super().__init__('Bad Request', httpcodes.HTTP_400_BAD_REQUEST)

class HttpExceptionUnauthorized(HttpException):
    def __init__(self):
        super().__init__('Not Authorized', httpcodes.HTTP_401_UNAUTHORIZED)

class HttpExceptionPermissionDenied(HttpException):
    def __init__(self):
        super().__init__('Permission Denied', httpcodes.HTTP_403_FORBIDDEN)

class HttpExceptionNotFound(HttpException):
    def __init__(self):
        super().__init__('Not Found', httpcodes.HTTP_404_NOT_FOUND)

class HttpExceptionCSRFFailure(HttpException):
    def __init__(self):
        super().__init__('CSRF Failure', httpcodes.HTTP_403_FORBIDDEN)

class HttpExceptionInternalServerError(HttpException):
    def __init__(self):
        super().__init__('Internal Server Error', httpcodes.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiException(HttpException):
    def __init__(self, msg, code=httpcodes.HTTP_422_UNPROCESSABLE_ENTITY, data={}):
        super().__init__(msg, code, data)

class ApiExceptionNotFound(ApiException):
    def __init__(self):
        super().__init__("HTTP 404 - Resource not found", code=httpcodes.HTTP_404_NOT_FOUND, data={})