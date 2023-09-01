from .base_mixins import BaseLoggingMixin


class LoggingMixin(BaseLoggingMixin):
    def initial(self, request, *args, **kwargs):
        print('*'*90)
        print('in logging mixin')
        # super() called the initial of the APIView(not the BaseLoggingMixin) in the Home view in views.py
        return super().initial(request, *args, **kwargs) 



    def finalize_response(self, request, response,*args, **kwargs):
        # super() called the finalize_response of the APIView(not the BaseLoggingMixin) in the Home view in views.py
        return super().finalize_response(request, response,*args, **kwargs)

