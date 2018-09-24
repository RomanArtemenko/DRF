from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'signup', views.SignUp)
router.register(r'signin', views.SignIn)

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('login', views.LoginView.as_view(), name='login'),
    # path('register', views.RegisterView.as_view(), name='register'),
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
    path(
        'test/fb/',
        views.FBSignIn.as_view(),
        name='xxx'
    ),
    # API
    path('api/v1.0/auth/', include(router.urls)),
]
