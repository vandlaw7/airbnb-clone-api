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
        # print(serializer)
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

    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None
    
    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = ReadRoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status = status.HTTP_404_NOT_FOUND)
  
    # update
    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # WirteRoomSerializer의 첫번째 argument로 room을 넣어주지 않으면,
            # update가 아니라 create로 인식한다. 반드시 넣어줘야 함.
            # partial을 넣어줌으로써 모든 required field를 입력하지 않아도 됨
            serializer = WriteRoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                # save를 하면 처음 만들어질 때는 serializer의 create 함수를,
                # 그 다음에 업데이트할 때부터는 update 함수를 실행시킨다.
                room = serializer.save()
                return Response(ReadRoomSerializer(room).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status = status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if room is not None:
            room.delete()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_404_NOT_FOUND)


