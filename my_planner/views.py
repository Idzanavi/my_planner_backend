from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from .models import User, PlannerItem
from .paginators import UserInfoPagination
from .serializers import RegistrationSerializer, PasswordChangeSerializer,\
    ItemSerializer, UserSerializer, UserInfoSerializer

from chat.event_logger import send_action_log

class WeekView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, week_no, *args, **kwargs):
        if "user" in self.kwargs:
            user_pk = self.kwargs["user"]
            items = PlannerItem.objects.filter(user__pk=user_pk, week_no=week_no)
        else:
            cur_user = request.user
            items = PlannerItem.objects.filter(user=cur_user, week_no=week_no)
        serializer = ItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, week_no):
        cur_user = request.user
        items = PlannerItem.objects.filter(user=cur_user, week_no=week_no)
        items.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

class FirstWeekNoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if "user" in self.kwargs:
            user_pk = self.kwargs["user"]
            items = PlannerItem.objects.filter(user__pk=user_pk).order_by('week_no')
        else:
            cur_user = request.user
            items = PlannerItem.objects.filter(user=cur_user).order_by('week_no')
        if not items:
            return Response(status=status.HTTP_404_NOT_FOUND)
        response_data = {'week_no': items[0].week_no}
        return Response(response_data)

class LastWeekNoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if "user" in self.kwargs:
            user_pk = self.kwargs["user"]
            items = PlannerItem.objects.filter(user__pk=user_pk).order_by('-week_no')
        else:
            cur_user = request.user
            items = PlannerItem.objects.filter(user=cur_user).order_by('-week_no')
        if not items:
            return Response(status=status.HTTP_404_NOT_FOUND)
        response_data = {'week_no': items[0].week_no}
        return Response(response_data)


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, week_no, day_no, slot_no,  *args, **kwargs):
        if "user" in self.kwargs:
            user_pk = self.kwargs["user"]
            item = get_object_or_404(PlannerItem, user__pk=user_pk, week_no=week_no, day_no=day_no, slot_no=slot_no)
        else:
            cur_user = request.user
            item = get_object_or_404(PlannerItem, user=cur_user, week_no=week_no, day_no=day_no, slot_no=slot_no)
        serializer = ItemSerializer(item, many=False, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        cur_user = request.user
        week_no = request.data["week_no"]
        day_no = request.data["day_no"]
        slot_no = request.data["slot_no"]
        item = ItemSerializer(data=request.data)
        if PlannerItem.objects.filter(user=cur_user, week_no=week_no, day_no=day_no, slot_no=slot_no).exists():
            raise ValidationError('This data already exists')
        if item.is_valid():
            item.save(user = cur_user)
            send_action_log("ADD", cur_user, item.data)
            return Response(item.data)
        else:
            raise ValidationError(item.errors)

    def delete(self, request, week_no, day_no, slot_no):
        cur_user = request.user
        item = get_object_or_404(PlannerItem, user=cur_user, week_no=week_no, day_no=day_no, slot_no=slot_no)
        serializer = ItemSerializer(item, many=False)
        send_action_log("DELETE", cur_user, serializer.data)
        item.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

    def patch(self, request, week_no, day_no, slot_no):
        cur_user = request.user
        item = get_object_or_404(PlannerItem, user=cur_user, week_no=week_no, day_no=day_no, slot_no=slot_no)
        data = ItemSerializer(instance=item, data=request.data, partial=True)
        if data.is_valid():
            data.save()
            send_action_log("UPDATE", cur_user, data.data)
            return Response(data.data)
        else:
            raise ValidationError(data.errors)


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if "user" in self.kwargs:
            user_pk = self.kwargs["user"]
            user = get_object_or_404(User, pk=user_pk)
        else:
            user = request.user
        serializer = UserSerializer(user, many=False, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        data = UserSerializer(instance=user, data=request.data, partial=True)
        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            raise ValidationError(data.errors)


class UsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = UserInfoPagination

    def get(self, request):
        users = User.objects.all().order_by('username')
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserInfoSerializer(page, many=True)
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
