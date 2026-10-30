
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Return a consistent error response for DRF exceptions.
    """
    response = exception_handler(exc, context)

    # Let Django handle unexpected exceptions.
    if response is None:
        return None

    response.data = {
        "success": False,
        "status_code": response.status_code,
        "errors": response.data,
    }

    return response
