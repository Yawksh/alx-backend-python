from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Only messages for the specified conversation (nested URL)
        return Message.objects.filter(conversation_id=self.kwargs['conversation_pk'])

    def perform_create(self, serializer):
        # Ensure the user is a participant before allowing message creation
        conversation = get_object_or_404(Conversation, conversation_id=self.kwargs['conversation_pk'])
        if self.request.user not in conversation.participants.all():
            raise ValidationError("User not in the conversation.")
        serializer.save(conversation=conversation, sender=self.request.user)
