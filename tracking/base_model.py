from django.db import models
from django.conf import settings


class BaseAPIRequestLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    # username, if username removed, username_persistent is exists 
    username_persistent = models.CharField(max_length=getattr(settings, 'DRF_TRACKING_LENGTH', 200), null=True, blank=True)
    requested_at = models.DateTimeField(db_index=True) # db_index is optional, it is used in databases
    response_ms = models.PositiveBigIntegerField(default=0)
    path = models.CharField(max_length=getattr(settings, 'DRF_TRACKING_PATH_LENGTH', 200), db_index=True)
    view = models.CharField(max_length=getattr(settings, 'DRF_TRACKING_VIEW_LENGTH', 200), null=True, blank=True, db_index=True, help_text='view called by this endpoint')
    view_method = models.CharField(max_length=getattr(settings, 'DRF_TRACKING_VIEW_METHOD_LENGTH', 200), null=True, blank=True, db_index=True)

    remote_addr = models.GenericIPAddressField()
    host = models.URLField()
    method = models.CharField(max_length=10)   # method: http method     view_method: methods in view class
    query_params = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True) # data that come from user like jsons
    response = models.TextField(null=True, blank=True) # response to user
    errors = models.TextField(null=True, blank=True)
    status_code = models.PositiveIntegerField(null=True, blank=True, db_index=True)


    class Meta:
        abstract = True  # data base not created for this model, because of abstract
        verbose_name = 'API Request Log'


    def __str__(self):
        return '{} {}'.format(self.method, self.path)