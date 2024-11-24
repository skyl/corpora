from functools import wraps

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


def async_raise_not_found(func):
    """Decorator to catch ObjectDoesNotExist and raise 404 in async views."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404("Object not found")

    return wrapper
