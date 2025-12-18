from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly  # custom permission

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing reviews.
    Only authenticated users can create reviews.
    Users can update/delete only their own reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Assign the logged-in user as the review's author.
        """
        serializer.save(user=self.request.user)
