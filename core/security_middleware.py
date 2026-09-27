"""
Lightweight security-header middleware for Sentinel Trinity.

Adds a Content-Security-Policy and Permissions-Policy to every response.
Kept dependency-free (no django-csp) so it works in any deployment target.
Adjust CSP_DIRECTIVES if you introduce external fonts/CDNs/analytics.
"""

CSP_DIRECTIVES = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data:; "
    "font-src 'self'; "
    "connect-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "object-src 'none'"
)

PERMISSIONS_POLICY = (
    "geolocation=(), microphone=(), camera=(), payment=(), usb=(), "
    "magnetometer=(), gyroscope=()"
)


class SecurityHeadersMiddleware:
    """Attaches CSP / Permissions-Policy / anti-caching headers for sensitive views."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault('Content-Security-Policy', CSP_DIRECTIVES)
        response.setdefault('Permissions-Policy', PERMISSIONS_POLICY)
        response.setdefault('X-Permitted-Cross-Domain-Policies', 'none')
        # This is an authorized-lab security tool — findings/evidence pages
        # must never be cached by intermediate proxies or the browser disk cache.
        response.setdefault('Cache-Control', 'no-store, max-age=0')
        return response
