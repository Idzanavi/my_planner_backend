from django.urls import path

from .views import RoomsView, ChatUsersView

urlpatterns = [
    path('api/users/', ChatUsersView.as_view()),
    path('api/rooms/', RoomsView.as_view()),
    path('api/rooms/', RoomsView.as_view()),
]