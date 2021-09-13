import functools
from django.http import Http404
from rest_framework.exceptions import PermissionDenied


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
        return wrapper_handleError

    return decorator_handleError
