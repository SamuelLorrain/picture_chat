from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

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
