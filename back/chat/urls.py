from django.urls import path, re_path
from . import views
from . import consumers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
]

urlpatterns = [

    path('messages/', views.getMessages),


    # authentication
    path(
        'tokens/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'tokens/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    )
]
