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


class UserSerializer(serializers.ModelSerializer):

    # write_only를 해 줌으로써 get 등으로 read할 때 비밀번호는 보이지가 않는다.
    # 안 보여도 password 값은 field 안에 명시돼 있으므로 post 요청으로부터 받아올 수 있다.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
            "password",
        )
        read_only_fields=("id", "superhost", "avatar")

    ''' You can specify custom field-level validation by adding .validate_<field_name> methods to your Serializer subclass. '''
    # validate_필드명 은 특별한 이름임. 알아서 value 값을 DRF가 찾아감.

    def validate_first_name(self, value):
        return value.upper()

    def create(self, validated_data):
        password = validated_data.get('password')
        user = super().create(validated_data)
        user.set_password(password)
        # user가 create되면서 자동으로 저장이 되고, set_password 해준 건 별도로 저장해야 함.
        user.save()
        return user