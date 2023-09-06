from django.urls import path
from . import views as test_views



urlpatterns = [
    path('no_logging/', test_views.MockNoLoggingView.as_view(), name='no_logging'),
    path('logging/', test_views.MockLoggingView.as_view(), name='with_logging'),
    path('explicit_logging/', test_views.MockExplicitLoggingView.as_view()),
    path('custom_check_logging/', test_views.MockCustomCheckLoggingView.as_view()),
    path('session_auth_logging/', test_views.MockSessionAuthLoggingView.as_view()),
    path('sensitive_fields_logging/', test_views.MockSensitiveFieldsView.as_view()),
    path('invalid_cleaned_sustitute_logging/', test_views.MockInvalidCleanedSubstituteLoggingView.as_view())

]