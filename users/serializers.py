from rest_framework import serializers
from .models import User


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost"
        )


class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            "groups",
            "user_permissions",
            "last_login",
            "password",
            "is_staff",
            "is_active",
            "is_superuser",
            "date_joined",
            "favs",
        )


class WriteUserSerialize(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )

    ''' You can specify custom field-level validation by adding .validate_<field_name> methods to your Serializer subclass. '''
    # validate_필드명 은 특별한 이름임. 알아서 value 값을 DRF가 찾아감.
    def validate_first_name(self, value):
        print(value)
        return value.upper()
