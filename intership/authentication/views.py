from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import urllib
import requests
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.views import View
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, SignUpSerializer, SignInSerializer
from intership.settings import OAUTH_CREDENTIALS
User = get_user_model()


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


class SignInFacebookView(View):
    template_name = "authentication/sign_in_facebook.html"
    errors = []
    authorize_url = 'https://www.facebook.com/v3.1/dialog/oauth?'

    clint_id = OAUTH_CREDENTIALS['facebook']['id']

    authorize_vars = {
        'client_id': clint_id,
        'redirect_uri':
        'http://localhost:8000/auth/facebook/redirect',
        # 'state': '{st=state123abc,ds=123456789}',
        'response_type': 'code',
        'scope': 'email'
    }

    url = authorize_url + urllib.parse.urlencode(authorize_vars)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.url)


class SignInFacebookRedirectView(View):
    template_name = "authentication/sign_in_facebook_redirect.html"
    clint_id = OAUTH_CREDENTIALS['facebook']['id']
    secret_key = OAUTH_CREDENTIALS['facebook']['secret']
    access_url = 'https://graph.facebook.com/v3.1/oauth/access_token?'
    access_vars = {
        'client_id': clint_id,
        'redirect_uri': 'http://localhost:8000/auth/facebook/redirect',
        'client_secret': secret_key,
        'code': ''
    }
    info_url = 'https://graph.facebook.com/v3.1/me?'
    info_vars = {
        'access_token': '',
        'fields': 'id,name,last_name,first_name,email',
        'format': 'json',
        'method': 'get',
        'pretty': '0',
        'suppress_http_code': '1'
    }

    def get(self, request, *args, **kwargs):
        if 'code' not in request.GET:
            return redirect('main')

        code = request.GET['code']
        self.access_vars.update({'code': code})
        url_at = self.access_url + urllib.parse.urlencode(self.access_vars)
        at = requests.get(url_at)
        access_token = at.json()['access_token']
        self.info_vars.update({'access_token': access_token})
        url_info = self.info_url + urllib.parse.urlencode(self.info_vars)
        user_info = requests.get(url_info)

        user, created = User.objects.get_or_create(
            email=user_info.json()['email']
        )
        if created:
            user.last_name = user_info.json()['last_name']
            user.first_name = user_info.json()['first_name']
            user.email = user_info.json()['name']
            user.save()

        return render(request, self.template_name, {
            'params': request.GET,
            'at': at.json(),
            'user_info': user_info.json()}
        )


class SignUp(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers({})
        out_serializer = UserSerializer(serializer.instance)
        return Response(out_serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)


class SignIn(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Token.objects.all()
    serializer_class = SignInSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers({})
        out_data = 'Token : %s' % serializer.instance.key
        return Response(out_data,
                        status=status.HTTP_200_OK, headers=headers)
