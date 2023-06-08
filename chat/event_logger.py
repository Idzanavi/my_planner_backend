from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ChatRoom

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
        'time': datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    }
    rooms = ChatRoom.objects.all()
    for room in rooms:
        room_group_name = 'room_%s' % room.name
        async_to_sync(channel_layer.group_send)(room_group_name, data)


def send_task_result(name, input, output, finished):
    channel_layer = get_channel_layer()
    data = {
        'type': 'task_status',
        'name': name,
        'input': input,
        'output': output,
        'finished': finished,
    }
    print("!!!!!!!!!!", name, input, output, finished)
    async_to_sync(channel_layer.group_send)('tasks', data)