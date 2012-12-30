from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.test import TestCase
from django.test.client import RequestFactory

from permissivecsrf.middleware import DisableCSRFMiddleware as _DisableCSRFMiddleware

class DisableCSRFMiddleware(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def tearDown(self):
        del self.factory

    def test_does_not_set_flag_when_debug_is_false(self):
        settings.DEBUG = False
        request = self.factory.get('/woot/')
        self.assertTrue(request.build_absolute_uri().startswith('http://'))
        self.assertFalse('HTTP_REFERER' in request.META)

        middleware = _DisableCSRFMiddleware()
        request = middleware.process_request(request)

        self.assertFalse(hasattr(request, '_dont_enforce_csrf_checks'))
