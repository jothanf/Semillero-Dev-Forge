from django.urls import path
from rest_framework.documentation import include_docs_urls
from .views import UserSignupView, UserSigninView, UserSignoutView, UserAgentSignupView, UserAgentSigninView, UserAgentSignoutView, UserCustomerSignupView, UserCustomerSigninView, UserCustomerSignoutView

urlpatterns = [
    path('api/signup/', UserSignupView.as_view(), name='signup'),
    path('api/signin/', UserSigninView.as_view(), name='signin'),
    path('api/signout/', UserSignoutView.as_view(), name='signout'),

    path('api/signup_agent/', UserAgentSignupView.as_view(), name='signup_agent'),
    path('api/signin_agent/', UserAgentSigninView.as_view(), name='signin_agent'),
    path('api/signout_agent/', UserAgentSignoutView.as_view(), name='signout_agent'),

    path('api/signup_customer/', UserCustomerSignupView.as_view(), name='signup_customer'),
    path('api/signin_customer/', UserCustomerSigninView.as_view(), name='signin_customer'),
    path('api/signout_customer/', UserCustomerSignoutView.as_view(), name='signout_customer'),

    path('docs/', include_docs_urls(title='docs'))
]