from django.conf import settings
try:
    from urllib import parse as urllib_parse
except ImportError:  # Python 2
    import urllib as urllib_parse
    import urlparse
    urllib_parse.urlparse = urlparse.urlparse


class PermissiveCSRFMiddleware(object):
    def process_request(self, request):
        # Only process in DEBUG
        if not settings.DEBUG:
            return

        ref = request.META.get('HTTP_REFERER')
        if ref is None or ref == '':
            return

        ref_parts = urllib_parse.urlparse(ref)
        if request.is_secure() and ref_parts.scheme == 'http':
            # CsrfViewMiddleware performs the following check through django.util.http.same_origin(ref, 'http://%s/' % request.get_host())
            # which fails when http://example.com/ posts to https://example.com/accounts/login
            # In our case we'll only check the hostname part
            dest = 'https://%s' % request.get_host()
            dest_parts = urllib_parse.urlparse(dest)
            same_origin = (ref_parts.hostname, ref_parts.port) == (dest_parts.hostname, dest_parts.port)
            # print 'ref=%s:%s dest=%s:%s ? %s' % (ref_parts.hostname, ref_parts.port, dest_parts.hostname, dest_parts.port, same_origin)
            if same_origin:
                setattr(request, '_dont_enforce_csrf_checks', True)
