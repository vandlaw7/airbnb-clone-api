from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import ReadUserSerializer, WriteUserSerialize
from rooms.serializers import RoomSerializer


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(ReadUserSerializer(request.user).data)

    def put(self, request):
        serializer = WriteUserSerialize(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response()


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(ReadUserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def toggle_fav(request):
#     room = request.data.get("room")
#     print(room) 

class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)
    
    # user의 favs를 업데이트하는 것일 뿐이다.새로 만드는 게 아니다.
    def put(self, request):
        pass

