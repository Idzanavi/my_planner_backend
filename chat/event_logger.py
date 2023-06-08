from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_action_log(action, user, item):
    channel_layer = get_channel_layer()
    data = {
        'type': 'log_event',
        'action': action,
        'user': user.username,
        'week': item['week_no'],
        'day': item['day_no'],
        'slot': item['slot_no'],
        'title': item['title'],
        'time': datetime.now()
    }
    group_keys = list(channel_layer.groups.keys())
    for key in group_keys:
        async_to_sync(channel_layer.group_send)(key, data)