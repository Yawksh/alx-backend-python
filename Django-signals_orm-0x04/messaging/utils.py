# messaging/utils.py

def build_thread_tree(messages):
    """
    Given a flat list of Message objects (with their .replies prefetched),
    build a nested structure:
      [ { msg: Message, replies: [ {...}, {...} ] }, ... ]
    """
    msg_map = {m.id: {'msg': m, 'replies': []} for m in messages}
    roots = []

    for m in messages:
        if m.parent_message_id:
            parent = msg_map.get(m.parent_message_id)
            if parent:
                parent['replies'].append(msg_map[m.id])
        else:
            roots.append(msg_map[m.id])

    return roots
