from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'email', 'first_name', 'last_name', 'phone_number')

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()  # additional read-only field via method:contentReference[oaicite:3]{index=3}
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ('message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'sender_name')
        read_only_fields = ('message_id', 'conversation', 'sender', 'sent_at', 'sender_name')

    def get_sender_name(self, obj):
        # Return sender's full name
        return f"{obj.sender.first_name} {obj.sender.last_name}"

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True)
    participant_count = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)  # nested messages:contentReference[oaicite:4]{index=4}

    class Meta:
        model = Conversation
        fields = ('conversation_id', 'participant_ids', 'participants', 'participant_count', 'messages')
        read_only_fields = ('conversation_id', 'participant_count', 'participants', 'messages')

    def get_participant_count(self, obj):
        return obj.participants.count()

    def validate_participant_ids(self, value):
        if len(value) < 2:
            # At least two participants required
            raise serializers.ValidationError("A conversation requires at least 2 participants.")  # validation example:contentReference[oaicite:5]{index=5}
        return value

    def create(self, validated_data):
        participants = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        return conversation
