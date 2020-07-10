from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room


class ReadRoomSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)


class WriteRoomSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField(help_text="USD per night")
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)

    
    # 항상 create를 통해 만들어진 objects를 반환해야 함. 
    # 안 그러면 에러 남: `create()` must be implemented.
    # 만든 후에 만들어진 객체를 프론트 단에 쏴줘서 유저에게 보여준다.
    def create(self, validated_data):
        ## **는 object의 unpacking을 의미함
        return Room.objects.create(**validated_data)

    # validate는 create와 마찬가지로 특별한 이름이다.
    # 이 이름이 아니면 자동으로 validation이 일어나지 않는다. 
    def validate(self, data): 
        # 이렇게 해주면 나중에 update할 때 validate 검사를 하지 않게 할 수 있다.
        if not self.instance:
            check_in = data.get('check_in')
            check_out = data.get('check_out')
            if check_in == check_out:
                raise serializers.ValidationError("Not enough time between changes")

        # 여기서 return data를 하지 않으면 위 함수의 
        # validated data에 data가 들어가지 않는다.
        return data

    def update(self, instance, validated_data):
        print(instance, validated_data )