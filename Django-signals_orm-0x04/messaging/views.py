

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message, Conversation
from .utils  import build_thread_tree  # from previous example
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')



# messaging/views.py


@login_required
def threaded_conversation(request, convo_id):
    # 1. Load the conversation (optional, for context)
    convo = get_object_or_404(Conversation, id=convo_id)

    # 2. Fetch *all* messages in this conversation by this user
    all_msgs = (
        Message.objects
               .filter(conversation=convo, sender=request.user)
               .select_related('sender', 'receiver')
               .prefetch_related('replies__sender', 'replies__replies')
    )
    #    ^^^^^ Message.objects.filter  ^^^^^ sender=request.user

    # 3. Build a nested tree of messages + replies
    thread_tree = build_thread_tree(all_msgs)

    # 4. Render in your template
    return render(request, 'messaging/threaded.html', {
        'conversation': convo,
        'thread_tree':  thread_tree,
    })
@login_required
def inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user).only(
        'id', 'sender', 'content', 'timestamp'
    )
    return render(request, 'messaging/inbox.html', {
        'unread_messages': unread_messages

    })
@cache_page(60)  # cache for 60 seconds
def conversation_detail(request, convo_id):
    convo = get_object_or_404(Conversation, id=convo_id)
    messages = convo.messages.select_related('sender').all()
    return render(request, 'chats/conversation_detail.html', {
        'conversation': convo,
        'messages': messages
    })