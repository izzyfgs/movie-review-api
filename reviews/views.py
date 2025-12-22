from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly  # custom permission
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly





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
        
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    # 🔍 filtering & search
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['movie_title', 'rating']
    search_fields = ['movie_title', 'content']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer


class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    search_fields = ['movie_title']

    filterset_fields = {
        'rating': ['gte', 'lte']
    }
# reviews/views.py

from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly  # Make sure this is imported

# Existing views (if any) go here...

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]



