from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def api_exception_handler(exc):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc)

    # Now add the HTTP status code to the response.
    if response is not None:
        if hasattr(exc, 'user_message'):
            response.data['user_message'] = exc.user_message
            del response.data['detail']
        if hasattr(exc, 'developer_message'):
            response.data['developer_message'] = exc.developer_message
        if hasattr(exc, 'code'):
            response.data['error_code'] = exc.code

    return response


class ApiException(APIException):

    def __init__(self, user_message=None, developer_message=None):
        self.user_message = user_message
        self.developer_message = developer_message
        self.detail = ""


class KeyDoesNotExistException(ApiException):
    code = 1
    status_code = 400


class DocumentDoesNotExistException(ApiException):
    code = 2
    status_code = 404


class MethodNotImplemented(ApiException):
    code = 3
    status_code = 400


class DocumentAlreadyExistsException(ApiException):
    code = 4
    status_code = 400


class MissingParameterException(ApiException):
    code = 5
    status_code = 400


class JsonDecodeException(ApiException):
    code = 6
    status_code = 400


class UnauthorizedException(ApiException):
    code = 7
    status_code = 401


class CommunicationErrorException(ApiException):
    code = 8
    status_code = 401


class BadArgumentErrorException(ApiException):
    code = 9
    status_code = 400
