import functools
from django.http import Http404
from rest_framework.exceptions import PermissionDenied, APIException


def handleError(target_object):
    def decorator_handleError(func):
        @functools.wraps(func)
        def wrapper_handleError(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except target_object.DoesNotExist:
                raise Http404
            except PermissionDenied as msg:
                raise PermissionDenied(msg)
            except AttributeError:
                pass
            except TypeError:
                raise BadRequest

        return wrapper_handleError

    return decorator_handleError


class BadRequest(APIException):
    status_code = 400
    default_detail = 'bad data recived, check the structure is needed by server to proccess'
    default_code = "bad request"
