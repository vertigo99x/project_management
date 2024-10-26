import logging

logger = logging.getLogger('django.request')

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request method and path
        logger.info(f"Request Method: {request.method}, Path: {request.path}")

        response = self.get_response(request)

        # Log the response status code
        logger.info(f"Response Status Code: {response.status_code}")

        return response
