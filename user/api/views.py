from user.api.serializers import *
from rest_framework.filters import OrderingFilter
from django.contrib.auth.models import User

from user.api.serializers import UserListSerializer
from utilities.views import QueryListAPIView

class UserListView(QueryListAPIView):

    # custom_related_fields = [""]
    # queryset = User.objects.select_related(*custom_related_fields).all()
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'


class ProfileListView(QueryListAPIView):

    custom_related_fields = ['user']
    queryset = Profile.objects.select_related(*custom_related_fields).all()
    serializer_class = ProfileListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'