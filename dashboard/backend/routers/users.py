from rest_framework import routers

from backend.views.users import UserViewSet

user_router = routers.DefaultRouter()
user_router.register(r'', UserViewSet)
