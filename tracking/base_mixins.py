from django.utils.timezone import now
import ipaddress



class BaseLoggingMixin:

    def initial(self, request, *args, **kwargs):

        self.log = {'requested_at': now()}# the key of dict shoul be the field name of BaseAPIRequest


        # super() called the initial of the APIView(not the BaseLoggingMixin) in the Home view in views.py
        return super().initial(request, *args, **kwargs) 



    def finalize_response(self, request, response,*args, **kwargs):
        
        self.log.update({
            'remote_addr': self._get_ip_address(request)
        })

        self.handle_log() # every thing in parrent is available in the childrens, so self.handle_log() is called by child in when
        # Home(LoggingMixin, APIView) => LoggingMixin(BaseLoggingMixin) => in BaseLogginMixin is self.handle_log() 



        # super() called the finalize_response of the APIView(not the BaseLoggingMixin) in the Home view in views.py
        return super().finalize_response(request, response,*args, **kwargs)
    


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