from urllib.parse import urlencode

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

class HttpErrorCodeResponse(Exception):
    def __init__(self, code, msg="Error"):
        self.code = code
        self.msg = msg

# Common errors
class HttpBadRequest(HttpErrorCodeResponse):
    def __init__(self):
        super().__init__(400, 'Bad Request')

class HttpUnauthorized(HttpErrorCodeResponse):
    def __init__(self):
        super().__init__(401, 'Not Authorized')

class HttpPermissionDenied(HttpErrorCodeResponse):
    def __init__(self):
        super().__init__(403, 'Permission Denied')

class HttpNotFound(HttpErrorCodeResponse):
    def __init__(self):
        super().__init__(404, 'Not Found')

class HttpCSRFFailure(HttpErrorCodeResponse):
    def __init__(self):
        super().__init__(403, 'CSRF Failure')

class HttpInternalServerError(HttpErrorCodeResponse):
    def __init__(self):
        super().__init__(500, 'Internal Server Error')
