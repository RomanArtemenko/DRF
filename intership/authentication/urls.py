from django.urls import path
from .views import MainView, SignInView, SignUpView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('sign-in', SignInView.as_view(), name='sign-in'),
    path('sign-up', SignUpView.as_view(), name='sign-up'),
]
