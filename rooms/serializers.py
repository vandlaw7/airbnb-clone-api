from rest_framework import serializers
from users.serializers import TinySerializer
from .models import Room



class RoomSerializer(serializers.ModelSerializer):

    user=TinySerializer()

    class Meta:
        model = Room
        fields = ("pk", "name", "price", "instant_book", "user")


class BigRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        exclude = ()
        # 이렇게 해도 됨
        # fields = "__all__"