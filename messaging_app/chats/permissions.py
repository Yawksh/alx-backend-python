# chats/permissions.py

from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users who are participants of the conversation
    to access or modify messages and conversations.
    """

    def has_permission(self, request, view):
        # This will cover the check for user.is_authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For Conversation
        if isinstance(obj, Conversation):
            if request.user in obj.participants.all():
                return True

        # For Message (which should have a conversation foreign key)
        if hasattr(obj, 'conversation'):
            if request.user in obj.conversation.participants.all():
                # Handle extra checks for modification requests (PUT/PATCH/DELETE)
                if request.method in ['PUT', 'PATCH', 'DELETE']:
                    return obj.sender == request.user  # Only sender can modify their message
                return True

        return False
