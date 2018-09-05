from django.shortcuts import render, redirect
from django.views import View
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, CustomUserSerializer


# Create your views here.

class MainView(View):
    template_name = "authentication/main.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class SignUpView(View):
    template_name = "authentication/sign_up.html"
    errors = []

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'errors': self.errors})

    def post(self, request, *args, **kwargs):
        return redirect('main')

class Signup(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return  UserSerializer
        else:
            self.serializer_class