from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterReceptionistSerializer, RegisterManagerSerializer
from .permissions import IsManager, IsReceptionist

CustomUser = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Assign permissions dynamically based on user role"""
        if self.action in ['register_manager']:
            self.permission_classes = []
        elif self.action in ['register_receptionist']:
            self.permission_classes = []
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsManager | IsReceptionist]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[])
    def register_receptionist(self, request):
        """Endpoint for creating a receptionist user"""
        serializer = RegisterReceptionistSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[])
    def register_manager(self, request):
        """Endpoint for creating a manager user"""
        serializer = RegisterManagerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
