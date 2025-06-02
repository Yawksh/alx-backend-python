from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()  # Nested serializer to include sender's details

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)  # Nested serializer for participants (users in the conversation)
    messages = MessageSerializer(many=True)  # Nested serializer for messages in the conversation

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages']

    # Optional method to customize how messages are retrieved, can be used if needed for specific cases
    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data
