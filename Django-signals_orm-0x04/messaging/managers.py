# messaging/managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Return only the fields we need (id, sender, content, timestamp)
        for messages received by `user` that are still unread.
        """
        return (
            super()
            .get_queryset()
            .filter(receiver=user, read=False
                    )
        )