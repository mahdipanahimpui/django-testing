from django.urls import path
from . import views as test_views



urlpatterns = [
    path('no_logging/', test_views.MockNoLoggingView.as_view(), name='no_logging'),
    path('logging/', test_views.MockLoggingView.as_view(), name='with_logging'),

]