from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class UnreadMessagesManager(models.Manager):
    def unread_for(self, user):
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only('id', 'sender', 'content', 'timestamp')
        )

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # ——— New for threading ———
    parent_message = models.ForeignKey(
        'self',
        null=True,        # top‑level if null
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )
    edited = models.BooleanField(default=False)
    # 🟡 New field to track read/unread status
    read = models.BooleanField(default=False)

    # 🔵 Attach managers
    objects = models.Manager()  # default manager
    unread_messages = UnreadMessagesManager()  # custom manager

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}…"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='histories')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User,on_delete  = models.CASCADE,related_name= 'updated_by')


