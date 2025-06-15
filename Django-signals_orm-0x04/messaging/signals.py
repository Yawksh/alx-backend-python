from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Message, Notification

@receiver(post_save, sender=Message)
def new_message_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old = Message.objects.get(pk=instance.pk)
        if old.content != instance.content:
            MessageHistory.objects.create(message=instance, old_content=old.content)
            instance.edited = True
@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    # Assuming on_delete=CASCADE cleans up most
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()