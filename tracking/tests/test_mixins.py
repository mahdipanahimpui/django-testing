from rest_framework.test import APITestCase, APIRequestFactory
from tracking.models import APIRequestLog
from django.test import override_settings
from . views import MockLoggingView, MockNoLoggingView


# Note ***** the path(url) is used as same as in url.py even slashes

@override_settings(ROOT_URLCONF='tracking.tests.urls') # override the settings.py when this class runs
class TestLoggingMixin(APITestCase):
    
    def test_nologing_no_log_created(self):
        self.client.get('/no_logging/') # because of using APITestCase Client obj is created befor, just use
        self.assertEqual(APIRequestLog.objects.all().count(), 0)

    def test_loging_log_created(self):
        self.client.get('/logging/') # because of using APITestCase Client obj is created befor, just use
        self.assertEqual(APIRequestLog.objects.all().count(), 1)


    def test_log_path(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        # print(APIRequestLog.objects.all().count())
        self.assertEqual(log.path, '/logging/')


    def test_log_ip_remote(self):
        # in APIRequestFactory the data of request is empty and rendering response is manually
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.1')


    def test_ip_remote_list(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '127.0.0.1, 127.0.0.2'
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.1')


    def test_ip_remote_with_port(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '127.0.0.1:8000'
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.1')


    def test_log_ip_remote_v6(self):
        request = APIRequestFactory().get('/logging/')
        ipv6_address = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        request.META['REMOTE_ADDR'] = ipv6_address
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '2001:db8:85a3::8a2e:370:7334')


    def test_log_ip_remote_v6_loopback(self):
        request = APIRequestFactory().get('/logging/')
        ipv6_address = "::1"
        request.META['REMOTE_ADDR'] = ipv6_address
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '::1')


    def test_log_ip_remote_v6_with_port(self):
        request = APIRequestFactory().get('/logging/')
        ipv6_address = "[::1]:8000"
        request.META['REMOTE_ADDR'] = ipv6_address
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '::1')



    def test_log_ip_remote_xforwarded(self):
        request = APIRequestFactory().get('/logging/')
        request.META['HTTP_X_FORWARDED_FOR'] = '127.0.0.1'
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.1')


    def test_log_ip_remote_xforwarded_list(self):
        request = APIRequestFactory().get('/logging/')
        request.META['HTTP_X_FORWARDED_FOR'] = '127.0.0.1, 127.0.0.2'
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.1')


    def test_log_host(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.host, 'testserver')


    def test_log_method(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.method , 'GET')


    def test_log_status_code(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.status_code , 200)

    



