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

    veriables = {
        'client_id': clint_id,
        'redirect_uri':
        'http://localhost:8000/auth/facebook/redirect',
        #'state': '{st=state123abc,ds=123456789}',
        'response_type': 'code',
        'scope': 'email'
    }

    url = authorize_url + urllib.parse.urlencode(veriables)

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

    def get(self, request, *args, **kwargs):
        if 'code' not in request.GET:
            return redirect('main')

        code = request.GET['code']

        self.access_vars.update({'code': code})

        url = self.access_url  + urllib.parse.urlencode(self.access_vars)

        at = requests.get(url)

        access_token = at.json()['access_token']
        # 'https://graph.facebook.com/v3.1/me?access_token=EAAGwgjSvQkoBABgGZAEZAwlhiGTtqlfzzcZCl5SeU3qoQgkapZBmXz3e1Bu1qXnwKBoD11I9ZBCBF0lZC7G51xdXPpO6w2z97SHGjyzr5fOVGzH8k8PjhBu6kvhVYD2ZAW8PiqtlFgsS3jA6vlQFcE7HMSkCJkwWSEEZA4k9MLW7XAZDZD&debug=all&fields=id%2Cname&format=json&method=get&pretty=0&suppress_http_code=1'

        user_info = requests.get('https://graph.facebook.com/v3.1/me?access_token=' + access_token + '&fields=id%2Cname%2Clast_name%2Cfirst_name%2Cemail%2Cgender&format=json&method=get&pretty=0&suppress_http_code=1')

        # user, created = User.objects.get_or_create(username=user_info.json()['name'])
        # if created:
        #     user.last_name = user_info.json()['last_name']
        #     user.first_name = user_info.json()['first_name']
        #     user.email = user_info.json()['email']
        #     user.save()

        user, created = User.objects.get_or_create(email=user_info.json()['email'])
        if created:
            user.last_name = user_info.json()['last_name']
            user.first_name = user_info.json()['first_name']
            user.email = user_info.json()['name']
            user.save()


        return  render(request, self.template_name, {'params': request.GET, 'at': at.json(), 'user_info': user_info.json()})


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


# class OAuthSignIn(object):
#     providers = None
#
#     def __init__(self, provider_name):
#         self.provider_name = provider_name
#         credentials = OAUTH_CREDENTIALS[provider_name]
#         self.consumer_id = credentials['id']
#         self.consumer_secret = credentials['secret']
#
#     def authorize(self):
#         pass
#
#     def callback(self):
#         pass
#
#     def get_callback_url(self):
#         return url_for('oauth_callback', provider=self.provider_name,
#                        _external=True)
#
#     @classmethod
#     def get_provider(self, provider_name):
#         if self.providers is None:
#             self.providers = {}
#             for provider_class in self.__subclasses__():
#                 provider = provider_class()
#                 self.providers[provider.provider_name] = provider
#         return self.providers[provider_name]
#
# class FacebookSignIn(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset =
#     serializer_class =
#
#     def __init__(self):
#         credentials = OAUTH_CREDENTIALS['facebook']
#         self.consumer_id = credentials['id']
#         self.consumer_secret = credentials['secret']
#         authorize_url = 'https://graph.facebook.com/oauth/authorize',
#         # https://www.facebook.com/v3.1/dialog/oauth
#         access_token_url = 'https://graph.facebook.com/oauth/access_token',
#         # https://graph.facebook.com/v3.1/oauth/access_token
#         base_url = 'https://graph.facebook.com/'
#
#     def authorize(self):
#         return redirect(self.service.get_authorize_url(
#             scope='email',
#             response_type='code',
#             redirect_uri=self.get_callback_url())
#         )
#
#     def callback(self):
#         pass
#
#     def get_callback_url(self):
#         pass
        # return url_for('oauth_callback', provider=self.provider_name,
        #                _external=True)


# {
#     status: 'connected',
#     authResponse: {
#         accessToken: '...',
#         expiresIn:'...',
#         signedRequest:'...',
#         userID:'...'
#     }
# }
#
# authResponse будет добавлен, если статус — connected и состоит из следующих элементов:
# accessToken — содержит маркер доступа для пользователя приложения.
# expiresIn — указывает UNIX-время, когда срок действия маркера истечет и его нужно будет обновить.
# signedRequest — параметр подписи, содержащий сведения о пользователе приложения.
# userID — указывает ID пользователя приложения.