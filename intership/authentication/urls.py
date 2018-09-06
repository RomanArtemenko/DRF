from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'signup', views.SignUp)
router.register(r'signin', views.SignIn)

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    # API
    path('api/v1.0/auth/', include(router.urls)),
]
