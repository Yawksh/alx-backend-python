from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Extended User Model
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
    max_length=15,
    unique=True,
    null=True,  # Temporary, remove after migration
    blank=True,  # Temporary, remove after migration
    # or add a proper default if appropriate
    default="0000000000"
)

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

# Conversation Model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')

    def __str__(self):
        return f"Conversation {self.conversation_id}"

# Message Model
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email} @ {self.sent_at}"
