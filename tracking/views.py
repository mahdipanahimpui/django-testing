from rest_framework.views import APIView
from rest_framework.response import Response
from . mixins import LoggingMixin

class Home(LoggingMixin, APIView): 
    # at first the method of the LoggingMixin like <initial> and <finalize_response> runs froms the first, not from the APIView,
    # Note APIView have the initial and finalize_response too
    # if call the super() in the initial and finalize_response of the LoggingMixin, the initial and finalize_response of the second calss(APIView) is called
    
    # logging_methods = ['GET', 'POST'] # overriding the logging_methods, <just log the get and post method>

    # def should_log(self, request, response): # could override the shoul_log
    #     return response.satatus_code >= 400

    # sensitive_fields = {'pass', 'email'} # sensitive_fields could override 

    def post(self, request):
        return Response('hello')