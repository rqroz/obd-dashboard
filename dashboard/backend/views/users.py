from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse

from rest_framework import viewsets, views
from rest_framework.decorators import renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from backend.serializers.users import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(is_staff=False, is_superuser=False).order_by('first_name', 'last_name')
    serializer_class = UserSerializer


class UserDetailsView(View):
    def get(self, request, format=None):
        return JsonResponse({'success': 'OK!'})
