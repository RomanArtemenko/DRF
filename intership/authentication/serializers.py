from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     min_length=1)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(max_length=30, min_length=2)
    last_name = serializers.CharField(max_length=30, min_length=2)
    password = serializers.CharField(max_length=128, min_length=8)
    confirm_password = serializers.CharField(max_length=128, min_length=8)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError(
                '"password" and "confirm_password" should be the same !'
            )

        return attrs

    def create(self, validated_data):
        user_data = dict(validated_data)
        user_data.pop('confirm_password')
        return User.objects.create_user(**user_data)


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, min_length=8)

    def create(self, validated_data):
        user = authenticate(
            email=validated_data['email'],
            password=validated_data['password']
        )



        if user is None:
            raise ValidationError('Wrong password')

        # login(user)

        token, created = Token.objects.get_or_create(user=user)
        return token


# class UserInfoSerializer(serializers.Serializer):
#     # user_data = {'id': '0', 'username': 'Anonimus'}
#     key = serializers.CharField(max_length=150,
#                                      min_length=1)
#
#     # def validate(self, attrs):
#     #     try:
#     #         token = Token.objects.get(key=attrs['key'])
#     #     except:
#     #         raise ValidationError('Incorrect key')
#     #         # return self.user_data
#     #
#     #     # self.user_data.update({'id': token.user.id})
#     #     # self.user_data.update({'username': token.user.username})
#     #
#     #     return attrs
#
#     def create(self, validated_data):
#         try:
#             token = Token.objects.get(key=validated_data['key'])
#         except:
#             raise ValidationError('Incorrect key')
#
#         # token, created = Token.objects.get_or_create(user=user)
#         # self.user_data.update({'id': token.user.id})
#         # self.user_data.update({'username': token.user.username})
#
#         # return self.user_data
#         return token

