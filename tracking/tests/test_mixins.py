from rest_framework.test import APITestCase, APIRequestFactory
from tracking.models import APIRequestLog
from django.test import override_settings
from . views import MockLoggingView, MockNoLoggingView
from unittest import mock
from django.contrib.auth.models import User
from tracking.mixins import BaseLoggingMixin
import ast
import datetime


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

    
    def test_logging_explicit(self):
        self.client.get('/explicit_logging/')
        self.client.post('/explicit_logging/')
        self.assertEqual(APIRequestLog.objects.all().count(), 1)

    
    def test_custom_check_logging(self):
        self.client.get('/custom_check_logging/')
        self.client.post('/custom_check_logging/')
        self.assertEqual(APIRequestLog.objects.all().count(), 1)


    def test_log_anon_user(self):
        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.user, None)


    def test_log_auth_user(self):
        User.objects.create_user(username='myname', password='000')
        user = User.objects.get(username='myname')

        self.client.login(username='myname', password='000')
        self.client.get('/session_auth_logging/')

        log = APIRequestLog.objects.first()
        self.assertEqual(log.user, user)

    
    def test_log_params(self):
        self.client.get('/logging/', {'p':'pp', 'c': 'cc'})
        log = APIRequestLog.objects.first()
        # print(log.query_params)
        # print(type(log.query_params)) # is str
        self.assertEqual(ast.literal_eval(log.query_params), {'p':'pp', 'c': 'cc'})

    
    def test_log_params_cleaned_from_personal_list(self):
        self.client.get('/sensitive_fields_logging/', {'SpEc_FiElD':'pp',  'not_import': 'not','key': 'cc'})
        log = APIRequestLog.objects.first()
        # print(log.query_params)
        # print(type(log.query_params)) # is str
        self.assertEqual(ast.literal_eval(log.query_params), {
            'SpEc_FiElD': BaseLoggingMixin.cleaned_substitude, 'not_import': 'not', 'key': BaseLoggingMixin.cleaned_substitude
              })
        

    def test_invalid_cleaned_substitute_fails(self):
        with self.assertRaises(AssertionError):
            self.client.get('/invalid_cleaned_sustitute_logging/')


    # check api works correct even the logging(LoggingMixin) fails
    @mock.patch('tracking.models.APIRequestLog.save')
    def test_log_doesnt_prevent_api_call_if_log_save_fails(self, mock_save): 
        mock_save.side_effect = Exception('db failure') # error of loggin module, to handle change the verbose level in settings.py by condition
        response = self.client.get('/logging/')
        self.assertEqual(response.status_code, 200) # api works correct
        self.assertEqual(APIRequestLog.objects.all().count(), 0) # bu APIRequestLogging not working


    @override_settings(USE_TZ=False) # to disable warning of timezone
    @mock.patch('tracking.base_mixins.now') # now method
    def test_log_doesnt_fail_with_negative_response_ms(self, mock_now):
        # each time mock_now is called, call one of below list
        # in the base_mixin now used twice, 
        # first in self.log = {'requested_at': now()}
        # second in _get_response_ms(self) 
        # mock_now[0] is used for first, mock_now[1] is used for second place
        mock_now.side_effect = [
            datetime.datetime(2017, 12, 1, 10, 0, 12),
            datetime.datetime(2017, 12, 1, 10, 0, 0),
        ]

        self.client.get('/logging/')
        log = APIRequestLog.objects.first()
        self.assertEqual(log.response_ms, 0)



