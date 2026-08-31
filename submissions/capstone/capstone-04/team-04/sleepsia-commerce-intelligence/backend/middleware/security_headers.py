"""
Security Headers Middleware - Add security headers to all responses
"""

import os
from django.utils.deprecation import MiddlewareMixin


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to all HTTP responses"""

    def process_response(self, request, response):
        """Add security headers to response"""

        # Prevent clickjacking attacks
        response['X-Frame-Options'] = 'DENY'

        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'

        # Enable XSS protection in browsers
        response['X-XSS-Protection'] = '1; mode=block'

        # Referrer Policy - Limit referrer information
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Permissions Policy - Restrict browser features
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'

        # Strict Transport Security (production only)
        if os.getenv('ENVIRONMENT') == 'production':
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'

        return response
