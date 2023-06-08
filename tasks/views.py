from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from tasks.tasks import prettify, send_mails

class PrettifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        prettify_task_id = prettify.delay(request.user.pk, request.user.username)
        return Response({'task_id': str(prettify_task_id)})


class SendMail(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        sendmail_task_id = send_mails.delay()
        return Response({'task_id': str(sendmail_task_id)})