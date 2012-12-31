from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from permissivecsrf.middleware import PermissiveCSRFMiddleware as _PermissiveCSRFMiddleware


class PermissiveCSRFMiddleware(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def tearDown(self):
        del self.factory

    def test_sets_flag_on_same_origin(self):
        settings.DEBUG = True
        factory = RequestFactory(**{'wsgi.url_scheme': 'https'})
        request = factory.get('/foo/')
        self.assertTrue(request.is_secure())

        referer = 'http://%s/' % request.get_host()
        request.META['HTTP_REFERER'] = referer
        self.assertTrue('HTTP_REFERER' in request.META)

        middleware = _PermissiveCSRFMiddleware()
        response = middleware.process_request(request)

        self.assertIsNone(response)
        self.assertTrue(hasattr(request, '_dont_enforce_csrf_checks'))
        self.assertTrue(getattr(request, '_dont_enforce_csrf_checks'))

    def _flag_not_set(self, request):
        middleware = _PermissiveCSRFMiddleware()
        response = middleware.process_request(request)

        self.assertIsNone(response)
        self.assertFalse(hasattr(request, '_dont_enforce_csrf_checks'))

    def test_does_not_set_flag_when_debug_is_false(self):
        settings.DEBUG = False
        request = self.factory.get('/foo/')
        self.assertTrue(request.build_absolute_uri().startswith('http://'))
        self.assertFalse('HTTP_REFERER' in request.META)

        self._flag_not_set(request)

    def test_does_not_set_flat_when_missing_http_referer(self):
        settings.DEBUG = True
        request = self.factory.get('/foo/')
        self.assertTrue(request.build_absolute_uri().startswith('http://'))
        self.assertFalse('HTTP_REFERER' in request.META)

        self._flag_not_set(request)

    def test_does_not_set_flag_if_destination_is_not_secure(self):
        settings.DEBUG = True
        request = self.factory.get('/foo/')
        request.META['HTTP_REFERER'] = 'http://example.com/'
        self.assertTrue(request.build_absolute_uri().startswith('http://'))
        self.assertTrue('HTTP_REFERER' in request.META)

        self._flag_not_set(request)

    def test_does_not_set_flag_if_origin_is_not_http_even_if_secure(self):
        settings.DEBUG = True
        factory = RequestFactory(**{'wsgi.url_scheme': 'https'})
        request = factory.get('/foo/')
        self.assertTrue(request.is_secure())

        request.META['HTTP_REFERER'] = 'https://example.com/'
        self.assertTrue('HTTP_REFERER' in request.META)

        self._flag_not_set(request)

    def test_does_not_set_flag_on_diff_origins(self):
        settings.DEBUG = True
        factory = RequestFactory(**{'wsgi.url_scheme': 'https'})
        request = factory.get('/foo/')
        self.assertTrue(request.is_secure())

        referer = 'http://foo.%s/' % request.get_host()
        request.META['HTTP_REFERER'] = referer
        self.assertTrue('HTTP_REFERER' in request.META)

        self._flag_not_set(request)

