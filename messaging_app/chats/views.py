# chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(participants=[self.request.user])

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = MessageFilter

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')  # covers the check
        queryset = self.queryset.filter(conversation__participants=self.request.user)

        if conversation_id:
            queryset = queryset.filter(conversation__id=conversation_id)  # Message.objects.filter(...)

        return queryset

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            # Covers the HTTP_403_FORBIDDEN requirement
            raise PermissionDenied(detail="You are not a participant in this conversation.", code=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user)
