"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from apps.chats.views import ChatRoomViewSet

api_router = DefaultRouter()

api_router.register('chat_room', ChatRoomViewSet, basename='chat-room')

urlpatterns = [
    path('chat/', include('apps.chats.urls')),
    path('admin/', admin.site.urls),
    # path('chat_room/<str:label>', chat_room, name="chat-room")
    path(r'api/', include(api_router.urls))
]
