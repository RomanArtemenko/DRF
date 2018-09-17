from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
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
from django.core.exceptions import ImproperlyConfigured
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


class Facebook():

    def __init__(self, conf_name):
        self.fields = ('client_id', 'secret', 'graph_root', 'access_url', 'authorize_url', 'info_url')

        self.settings = self.get_setings(conf_name)
        self.fields_initialization()
        self.authorize_vars = {
            'client_id': '',
            'redirect_uri': '',
            'response_type': 'code',
            'scope': 'email'
        }
        self.access_vars = {
            'client_id': '',
            'redirect_uri': '/auth/facebook/redirect',
            'client_secret': '',
            'code': ''
        }
        self.info_vars = {
            'access_token': '',
            'fields': 'id,name,last_name,first_name,email',
            'format': 'json',
            'method': 'get',
            'pretty': '0',
            'suppress_http_code': '1'
        }
        # self.clint_id = self.get_client_id()
        # self.secret_key = self.get_secret_key()
        # self.access_url = self.get_access_url()
    # access_vars = settings.get('access_vars')
    #     self.authorize_url = self.get_authorize_url()
    # authorize_vars = settings.get('authorize_vars')
    #     self.info_url = self.get_info_url()
    #     self.info_vars = settings.get('info_vars')

    def get_setings(self, social_name):
        if OAUTH_CREDENTIALS.get(social_name) is None:
            raise ImproperlyConfigured(
                "There is no such configuration !" )
        else:
            return OAUTH_CREDENTIALS.get(social_name)

    def fields_initialization(self):
        for field in self.fields:
            if self.settings.get(field) is None:
                raise ImproperlyConfigured(
                    "%s does not exist !" % field)
            else:
                setattr(self, field, self.settings.get(field))

    def get_access_url(self):
        return '%s%s' % (self.graph_root, self.access_url)

    def get_info_url(self):
        return '%s%s' % (self.graph_root, self.info_url)

    def authorize(self, request, redirec_point):
        url_fb = request.build_absolute_uri(
            reverse(redirec_point)
        )

        self.authorize_vars.update({'client_id': self.client_id})
        self.authorize_vars.update({'redirect_uri': url_fb})
        url = self.authorize_url + urllib.parse.urlencode(self.authorize_vars)
        # return HttpResponseRedirect(url)
        return url


class SignInFacebookView(View):
    template_name = "authentication/sign_in_facebook.html"
    errors = []
    fb = Facebook('facebook')

    # authorize_url = OAUTH_CREDENTIALS.get('facebook').get('authorize_url')
    # clint_id = OAUTH_CREDENTIALS.get('facebook').get('id')
    #
    # authorize_vars = OAUTH_CREDENTIALS.get('facebook').get('authorize_vars')

    def get(self, request, *args, **kwargs):
        # url_fb = request.build_absolute_uri(
        #     reverse('sign-in-facebook-redirect')
        # )
        #
        # self.authorize_vars.update({'client_id': self.clint_id})
        # self.authorize_vars.update({'redirect_uri': url_fb})
        # url = self.authorize_url + urllib.parse.urlencode(self.authorize_vars)

        return HttpResponseRedirect(self.fb.authorize(request, 'sign-in-facebook-redirect'))


class SignInFacebookRedirectView(View):
    template_name = "authentication/sign_in_facebook_redirect.html"
    fb = Facebook('facebook')

    def get(self, request, *args, **kwargs):
        if 'code' not in request.GET:
            return redirect('main')

        code = request.GET.get('code')
        self.fb.access_vars.update({'client_id': self.fb.client_id})
        self.fb.access_vars.update({'code': code})
        url_at = self.fb.get_access_url() + urllib.parse.urlencode(self.fb.access_vars)
        at = requests.get(url_at).json()
        access_token = at.get('access_token')
        self.fb.info_vars.update({'access_token': access_token})
        url_info = self.fb.get_info_url() + urllib.parse.urlencode(self.fb.info_vars)
        user_info = requests.get(url_info).json()

        user, created = User.objects.get_or_create(
            email=user_info.get('email')
        )
        if created:
            user.last_name = user_info.get('last_name')
            user.first_name = user_info.get('first_name')
            user.username = user_info.get('name')
            user.save()

        token, created = Token.objects.get_or_create(user=user)

        return render(request, self.template_name, {
            'params': request.GET,
            'at': at,
            'user_info': user_info,
            'token': 'Token %s' % token}
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
        out_data = 'Token %s' % serializer.instance.key
        return Response(out_data,
                        status=status.HTTP_200_OK, headers=headers)


# class Profile(viewsets.views.APIView):
#     serializer_class = UserSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         serializer = self.serializer_class(user)
#         return Response(serializer.data)


# class  UserInfo(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     queryset = User.objects.none()
#     serializer_class = UserSerializer
#
#     def get_object(self):
#         return self.request.user
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         # instance = request.user
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)


class  Profile(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.none()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_authenticated:
            return Response({'username': 'Anonymous'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
