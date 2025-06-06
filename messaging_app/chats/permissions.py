# chats/permissions.py

from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the object is a Conversation
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        # Check if the object has a conversation (e.g., Message)
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False
