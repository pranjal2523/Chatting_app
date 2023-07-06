from django.urls import path
from .views import (
    register_user,
    login_user,
    LogoutView,
    chat,
    create_chat,
    chatview,
    post,
    )


urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', LogoutView, name='logout_user'),
    path('chat/', chat, name='chat'),
    path('create_chat/<str:recieveremail>', create_chat , name='create_chat'),
    path('chatview/<int:chat_id>', chatview , name='chatview'),
    path('post', post, name='post'),
]