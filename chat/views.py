import datetime
import math

from channels.layers import get_channel_layer
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from chat.models import ChatUser
from chat.paginators import ChatUserPagination
from chat.serializers import ChatUserSerializer
from chat.utils import prefix_remover


class ChatUsersView(APIView):
    permission_classes = [permissions.IsAdminUser]
    pagination_class = ChatUserPagination

    def get(self, request):
        chat_users = ChatUser.objects.all().order_by('username')
        page = self.paginate_queryset(chat_users)
        if page is not None:
            serializer = ChatUserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)


class RoomsView(APIView):
    items_per_page = 10

    def get(self, request, *args, **kwargs):
        channel_layer = get_channel_layer()
        rooms = channel_layer.groups.keys()
        rooms_num = len(rooms)
        pages_num = math.ceil(rooms_num / self.items_per_page)
        page_no = 1
        if "page" in self.kwargs:
            page = self.kwargs["page"]
            if page >= 1 and page <= pages_num:
                page_no = page
        if rooms_num == 0:
            rooms_data = []
        else:
            start_idx = (page_no - 1) * self.items_per_page
            end_idx = min(start_idx + self.items_per_page, rooms_num)
            rooms_data = map(prefix_remover('room_'), list(rooms)[start_idx: end_idx])
        data = {
            'count': rooms_num,
            'page': page_no,
            'pages': pages_num,
            'rooms': rooms_data
        }
        return Response(data)