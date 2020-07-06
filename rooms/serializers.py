from rest_framework import serializers
from users.serializers import TinySerializer
from .models import Room



class RoomSerializer(serializers.ModelSerializer):

    user=TinySerializer()

    class Meta:
        model = Room
        fields = ("name", "price", "instant_book", "user")