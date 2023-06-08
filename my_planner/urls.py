from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .views import WeekView, FirstWeekNoView, LastWeekNoView, \
    RegistrationView, ChangePasswordView, ItemView, UserView, UsersView

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('week/<int:week_no>/', WeekView.as_view(http_method_names=('get', 'delete'))),
    path('week/<int:user>/<int:week_no>/', WeekView.as_view(http_method_names=('get',))),
    path('first-week/', FirstWeekNoView.as_view()),
    path('first-week/<int:user>/', FirstWeekNoView.as_view()),
    path('last-week/', LastWeekNoView.as_view()),
    path('last-week/<int:user>/', LastWeekNoView.as_view()),
    path('register/', RegistrationView.as_view()),
    path('change-pwd/', ChangePasswordView.as_view()),
    path('item/', ItemView.as_view(http_method_names=('post',))),
    path('item/<int:week_no>/<int:day_no>/<int:slot_no>/', ItemView.as_view(http_method_names=('get', 'delete', 'patch',))),
    path('item/<int:user>/<int:week_no>/<int:day_no>/<int:slot_no>/', ItemView.as_view(http_method_names=('get',))),
    path('user/', UserView.as_view(http_method_names=('get', 'patch'))),
    path('user/<int:user>/', UserView.as_view(http_method_names=('get'))),
    path('users/', UsersView.as_view()),
]