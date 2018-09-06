from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30, min_length=2)
    last_name = serializers.CharField(max_length=30, min_length=2)
    password = serializers.CharField(max_length=128, min_length=8)
    confirm_password = serializers.CharField(max_length=128, min_length=8)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError('"username" and "confirm_username" should be the same !')

        return attrs

    def create(self, validated_data):
        user_data = dict(validated_data)
        user_data.pop('confirm_password')
        return User.objects.create_user(**user_data)