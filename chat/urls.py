from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView, name="login"),
    path('register/', views.register, name="register"),
    path('room/', views.indexChatRoom, name="index"),
    path('room/<int:pk>/', views.showChatRoom, name="show_room"),
    path('room/<int:pk>/create/', views.createChatRoom, name="create_room"),
    path('room/<int:pk>/message/', views.sendMessage, name="send_message")
]
