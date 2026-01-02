from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# CHANGE THIS: Import UserSerializer instead of RegisterSerializer
from .serializers import UserSerializer 

class RegisterView(generics.CreateAPIView):
    # CHANGE THIS: Point to UserSerializer
    serializer_class = UserSerializer
    
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": {
                    "username": user.username,
                    "email": user.email
                },
                "message": "User created successfully. You can now login."
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
