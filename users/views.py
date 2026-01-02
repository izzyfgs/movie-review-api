from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    # This tells DRF which fields (username, email, password) to display
    serializer_class = RegisterSerializer
    
    # This allows users who aren't logged in to see and use the form
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
