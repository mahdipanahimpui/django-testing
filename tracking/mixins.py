from .base_mixins import BaseLoggingMixin
from .models import APIRequestLog


class LoggingMixin(BaseLoggingMixin):
    
    def handle_log(self):
        print(self.log)
        # APIRequestLog(**self.log).save() # to open dict, using the class name means create the objdect of that class



