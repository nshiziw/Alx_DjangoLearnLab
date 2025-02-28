from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class CSPMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self';"
        return response
