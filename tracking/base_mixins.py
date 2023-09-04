from django.utils.timezone import now
import ipaddress
from . app_settings import app_settings
import traceback
import logging
import ast

logger = logging.getLogger(__name__)

class BaseLoggingMixin:
    logging_methods = '__all__' # could override i view classes
    sensitive_fields = {} # a set, override by user
    cleaned_substitude = "*" # use to replace with sensitive fields

    def initial(self, request, *args, **kwargs):

        self.log = {'requested_at': now()}# the key of dict shoul be the field name of BaseAPIRequest


        # super() called the initial of the APIView(not the BaseLoggingMixin) in the Home view in views.py
        return super().initial(request, *args, **kwargs) 

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        self.log['errors'] = traceback.format_exc() # convert the raised error to string
        return response

    def finalize_response(self, request, response,*args, **kwargs):
        response = super().finalize_response(request, response,*args, **kwargs)

        if self.should_log(request, response):

            user = self._get_user(request)

            # Note: var defined in inner if is available in outer if or for
            if response.streaming:
                rendered_content = None
            elif hasattr(response, 'rendered_content'):
                rendered_content = response.rendered_content
            else:
                rendered_content = response.getvalue()
                

            print(rendered_content)

        

            self.log.update({
                'remote_addr': self._get_ip_address(request),
                'view': self._get_view_name(request),
                'view_method': self._get_veiw_method(request),
                'path': self._get_path(request),
                'host': request.get_host(),
                'method': request.method,
                'user': user,
                'username_persistent': user.get_username() if user else "Anonymous",  # get_username is for django
                'response_ms': self._get_response_ms(),
                'status_code': response.status_code,
                'query_params': self._clean_data(request.query_params.dict()),
                'response': self._clean_data(rendered_content)
        })
            try:
                self.handle_log() # every thing in parrent is available in the childrens, so self.handle_log() is called by child in when
                # Home(LoggingMixin, APIView) => LoggingMixin(BaseLoggingMixin) => in BaseLogginMixin is self.handle_log() 
                # print('self in self.handle_log(): ', self) # <tracking.views.Home object at 0x7f3c3c495c50>
            except Exception:
                logger.exception('logging API cal raise exception')


        # super() called the finalize_response of the APIView(not the BaseLoggingMixin) in the Home view in views.py
        return response
    

    def handle_log(self):
        raise NotImplemented # to force the child to over ride this method to use in finalize_response
    


    def _get_ip_address(self, request):


    # attrs in request.META to get ip
        # REMOTE_ADDR => the presented ip (real ip or proxy ip)
        # HTTP_X_FORWARDED_FOR => real_ip, 1st_proxy, 2nd_proxy, last_poxy


        ipaddr = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if ipaddr:
            ipaddr = ipaddr.split(',')[0] # take the real ip

        else:
            ipaddr = request.META.get('REMOTE_ADDR', '').split(',')[0] # .split(',')[0] is used to make sure just getting one ip
            
            # ip formats:
                # <ipv4> #<ipv6> #<ipv4>:port #[<ipv6>]:port
            # so handle to get just ipv4/6 not port or list

            # lstrip('[') remover the '[' until is not the first char
            possibles = (ipaddr.lstrip('[').split(']'), ipaddr.split(':')[0]) # it is a tuple index0 handle the first, second and 4th posibles and the index1 handle the third one.

            for addr in possibles:
                try:
                    return str(ipaddress.ip_address(addr))  # return the ip by its type v4 or v6 in result
                except:
                    pass

            return addr
        

    def _get_view_name(self, request):
        method = request.method.lower()
        # print(self) # <tracking.views.Home object at 0x7f989f747dd0>
        # print(getattr(self, method)) # <bound method Home.get of <tracking.views.Home object at 0x7f3c3c495c50>>
        try:
            attr = getattr(self, method)
            # print(type(attr.__self__)) # <class 'tracking.views.Home'>
            return type(attr.__self__).__module__ + '.' + type(attr.__self__).__module__
        except AttributeError:
            return None
        

    def _get_veiw_method(self, request): 
        if hasattr(self, 'action'):
            return self.action or None
        return request.method.lower()


    def _get_path(self, request):
        return request.path[:app_settings.PATH_LENGTH]
    

    def _get_user(self, request):
        user = request.user
        if user.is_anonymous:
            return None
        return user
    

    def _get_response_ms(self):
        response_timedelta = now() - self.log['requested_at']
        response_ms = int(response_timedelta.total_seconds() * 1000) # to convet mili seconds
        return max(response_ms, 0)
    

    # with wich condition logging, (could override by user)
    def should_log(self, request, response): 
        # if __all__ return true else return true if the method exists in the logging_methods
        return (
            self.logging_methods == '__all__' or request.method in self.logging_methods
        )
    

    def _clean_data(self, data):

        if isinstance(data, list):
            return [self._clean_data(d) for d in data if isinstance(d, dict)] # if list of dict is passed

        elif isinstance(data, dict):
            SENSITIVE_FIELDS = {'api', 'token', 'key', 'secret', 'signature'}

            if self.sensitive_fields:
                # to add to set use |
                SENSITIVE_FIELDS = SENSITIVE_FIELDS | {field.lower() for field in self.sensitive_fields}

            for key, value in data.items():

                try:
                    value = ast.literal_eval(value) # literal_eval returns python syntax, ex) if value is like "{'name': 'hello'}" result is {'name': 'hello'}
                except (ValueError, SyntaxError):
                    pass # because the value is not literal_eval

                if isinstance(value, (list, dict)):
                    data[key] = self._clean_data(value)
                
                if key.lower() in SENSITIVE_FIELDS:
                    data[key] = self.cleaned_substitude

        return data