# chats/urls.py

from django.urls import path, include

from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Create a DefaultRouter instance
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
# Include the router.urls in urlpatterns
urlpatterns = [
    path("", ConversationViewSet),
    path('', include(router.urls)),]
