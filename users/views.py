from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ReadUserSerializer, WriteUserSerialize
from .models import User


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

