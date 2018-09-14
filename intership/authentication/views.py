from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from rest_framework.authtoken.views import ObtainAuthToken
import urllib
import requests
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.views import View
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, SignUpSerializer, SignInSerializer
from intership.settings import OAUTH_CREDENTIALS
from rest_framework import permissions
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
        'redirect_uri': '',
        # 'state': '{st=state123abc,ds=123456789}',
        'response_type': 'code',
        'scope': 'email'
    }

    def get(self, request, *args, **kwargs):
        url_fb = request.build_absolute_uri(
            reverse('sign-in-facebook-redirect')
        )
        self.authorize_vars.update({'redirect_uri': url_fb})
        url = self.authorize_url + urllib.parse.urlencode(self.authorize_vars)
        return HttpResponseRedirect(url)


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


class LoginView(View):
    template_name = "authentication/login.html"
    errors = []

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'errors': self.errors})

    def post(self, request, *args, **kwargs):
        return redirect('main')


class RegisterView(View):
    template_name = "authentication/register.html"
    errors = []

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'errors': self.errors})

    def post(self, request, *args, **kwargs):
        return redirect('main')


#API view
# class SignUp(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = SignUpSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers({})
#         out_serializer = UserSerializer(serializer.instance)
#         return Response(out_serializer.data,
#                         status=status.HTTP_201_CREATED, headers=headers)
#
#
class SignIn(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Token.objects.all()
    serializer_class = SignInSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers({})
        out_data = 'Token %s' % serializer.instance.key
        return Response(out_data,
                        status=status.HTTP_200_OK, headers=headers)


class Profile(viewsets.views.APIView):
    # queryset = User.objects.none()
    serializer_class = UserSerializer

    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        # serializer = self.serializer_class(data=request.data,
        #                                    context={'request': request})
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        # token, created = Token.objects.get_or_create(user=user)

        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    # lookup_field = 'key'
    # lookup_value_regex = '[0-9a-f]'

    # def retrieve(self, request, *args, **kwargs):
    #     # instance = self.get_object()
    #     serializer = self.get_serializer(data=request.data)
    #     return Response(serializer.data)

# class  UserInfo(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     queryset = User.objects.none()
#     serializer_class = UserInfoSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers({})
#         # out_serializer = UserSerializer(serializer.instance)
#         out_serializer = {
#             'id': serializer.instance.user.pk,
#             'username': serializer.instance.user.username
#         }
#         return Response(out_serializer,
#                         status=status.HTTP_201_CREATED, headers=headers)


# class UserViewSet(ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class CustomAuthToken(ObtainAuthToken):
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})