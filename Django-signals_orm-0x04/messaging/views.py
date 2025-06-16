

from django.shortcuts import render, get_object_or_404
from .models import Message@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')



def conversation_thread(request, convo_id):
    # 1. Fetch top‑level messages in this conversation
    top_level = (
        Message.objects
               .filter(conversation_id=convo_id, parent_message__isnull=True)
               .select_related('sender', 'receiver')           # join sender/receiver
               .prefetch_related(
                   'replies__sender',     # for each reply, also join its sender
                   'replies__replies'     # prefetch nested replies (one level deep)
               )
    )

    context = {'threads': top_level}
    return render(request, 'messaging/thread_list.html', context)
