from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer

class RoomsView(APIView):

    def get(self, request):
        rooms = Room.objects.all()[:5]
        # 이 건 json이 아니라 변환된 결과 나타난 python dictionary다.
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            # create를 직접 call하지 않고 save method를 call해야 한다.
            # create인지 update인지 serializer가 알아냄
            # 처음 불렸으면 create 그 이후엔 update
            #save함수의 kwagrs에 들어가는 것들은 validated data에 다 들어간다
            room = serializer.save(user=request.user)
            room_serializer = ReadRoomSerializer(room)
            return Response(data=room_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    
    def get(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            serializer = ReadRoomSerializer(room).data
            return Response(serializer)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        pass

    def delete(self, request):
        pass


