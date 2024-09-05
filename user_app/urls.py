from django.urls import path
from rest_framework.documentation import include_docs_urls
from .views import (
    UserAgentSignupView, 
    UserSigninView, 
    UserAgentSignoutView,
    UserCustomerInitialSignupView,
    UserCustomerCompleteSignupView,
    UserCustomerSignoutView
)

urlpatterns = [
    path('api/signup_agent/', UserAgentSignupView.as_view(), name='signup_agent'),
    path('api/signout_agent/', UserAgentSignoutView.as_view(), name='signout_agent'),

    path('api/signup_customer_initial/', UserCustomerInitialSignupView.as_view(), name='signup_customer_initial'),
    path('api/signup_customer_complete/', UserCustomerCompleteSignupView.as_view(), name='signup_customer_complete'),

    path('api/signout_customer/', UserCustomerSignoutView.as_view(), name='signout_customer'),

    path('api/signin/', UserSigninView.as_view(), name='signin'),

    path('docs/', include_docs_urls(title='API Documentation')),
]
