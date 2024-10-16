from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from .pagination import StandardResultSetPagination
from .permissions import IsUser


class UserListView(APIView, StandardResultSetPagination):
    def get(self, request):
        queryset = User.objects.all()
        result = self.paginate_queryset(queryset, request)
        serializer = UserSerializer(instance=result, many=True)
        return self.get_paginated_response(serializer.data)


class UserDetailView(APIView):
    permission_classes = (IsUser, IsAuthenticated)

    def get(self, request, pk):
        instance = User.objects.get(id=pk)
        serializer = UserSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(data=request.data, instance=user, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, reqeust, pk):
        instance = User.objects.get(id=pk)
        instance.delete()
        return Response({'response': 'user deleted'})


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # If you need to set a password or do other custom actions, you can do it here
        user = serializer.save()
        user.set_password(user.password)
        user.save()


