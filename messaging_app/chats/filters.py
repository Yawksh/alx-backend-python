# chats/filters.py

import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    sender_id = django_filters.NumberFilter(field_name='sender__id')

    class Meta:
        model = Message
        fields = ['conversation', 'sender_id', 'sent_after', 'sent_before']
