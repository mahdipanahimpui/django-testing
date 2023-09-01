from django.utils.timezone import now




class BaseLoggingMixin:

    def initial(self, request, *args, **kwargs):
        print('helllllo')
        # super() called the initial of the APIView(not the BaseLoggingMixin) in the Home view in views.py
        return super().initial(request, *args, **kwargs) 



    def finalize_response(self, request, response,*args, **kwargs):

        # super() called the finalize_response of the APIView(not the BaseLoggingMixin) in the Home view in views.py
        return super().finalize_response(request, response,*args, **kwargs)