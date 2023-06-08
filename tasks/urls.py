from django.urls import path

from .views import PrettifyView, SendMail

urlpatterns = [
    path('api/prettify/', PrettifyView.as_view()),
    path('api/sendmail/', SendMail.as_view()),
]