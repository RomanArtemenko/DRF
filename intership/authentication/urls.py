from django.conf.urls import url
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter


router = DefaultRouter()
# router = SimpleRouter()
router.register(r'signin', views.SignIn)
# router.register(r'signup', views.SignUp)
# router.register(r'profile', views.Profile)


urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path(
        'auth/facebook',
        views.SignInFacebookView.as_view(),
        name='sign-in-facebook'
    ),
    path(
        'auth/facebook/redirect',
        views.SignInFacebookRedirectView.as_view(),
        name='sign-in-facebook-redirect'
    ),
    # url(r'^profile', views.CustomObtainAuthToken.as_view()),
    path('profile/', views.CustomObtainAuthToken.as_view()),
    path('xxx/', views.Profile.as_view()),
    # API
    #path('api/v1.0/auth/', include(router.urls)),
    url(r'api/v1.0/auth/', include(router.urls)),

]
