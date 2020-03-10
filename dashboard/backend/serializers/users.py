from django.contrib.auth.models import User

from rest_framework import serializers

from backend.models.users import UserDetails


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['pk', 'img']


class UserSerializer(serializers.ModelSerializer):
    details = UserDetailsSerializer()

    class Meta:
        model = User
        fields = ['pk', 'first_name', 'last_name', 'email', 'details']
