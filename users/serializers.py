from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("groups", "user_permissions", "last_login",
                   "password", "is_staff", "is_active", "is_superuser",
                   "favs")
