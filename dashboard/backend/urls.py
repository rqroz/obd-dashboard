from django.urls import path, include

from backend.routers.users import user_router
from backend.views.users import UserDetailsView
from backend.views.external import external_input

urlpatterns = [
    path('users/', include(user_router.urls)),
    path('self/', UserDetailsView.as_view(), name='self_view'),
    path('external/', external_input, name='external_input'),
]
