from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room


class ReadRoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()

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
        # 이렇게 해주면 update와 create를 구별해서 처리해줄 수 있다.
        # instance 존재하면 update mode인 것임
        if self.instance:
            # 만약 partial update라서 체크인 체크 아웃을 안 넣어줬다면 None이 들어가므로
            # 디폴트 값 지정해준 것이다.
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get('check_in')
            check_out = data.get('check_out')
        if check_in == check_out:
            raise serializers.ValidationError(
                "Not enough time between changes")

        # 여기서 return data를 하지 않으면 위 함수의
        # validated data에 data가 들어가지 않는다.
        return data 

    def update(self, instance, validated_data):
        # 이렇게 해주면 partial update 해준 항목만 새로 넣어주고, 
        # 나머지는 기존 것 그대로 넣어줄 수 있음.
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.price = validated_data.get("price", instance.price)
        instance.beds = validated_data.get("beds", instance.beds)
        instance.lat = validated_data.get("lat", instance.lat)
        instance.lng = validated_data.get("lng", instance.lng)
        instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
        instance.bathrooms = validated_data.get(
            "bathrooms", instance.bathrooms)
        instance.check_in = validated_data.get("check_in", instance.check_in)
        instance.check_out = validated_data.get(
            "check_out", instance.check_out)
        instance.instant_book = validated_data.get(
            "instant_book", instance.instant_book)
        instance.save()
        return instance
