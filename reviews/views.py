from rest_framework import generics, permissions, filters
from .models import Review
from .serializers import ReviewSerializer

# Only owner can edit/delete
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return obj.user == request.user

# List and Create reviews
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # <-- No DjangoFilterBackend
    search_fields = ['movie_title']
    ordering_fields = ['rating', 'created_date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Retrieve, Update, Delete
class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]



from rest_framework import generics, permissions, filters
from .models import Review
from .serializers import ReviewSerializer

# Only owner can edit/delete
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Anyone can read
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only the owner can edit/delete
        return obj.user == request.user

# List and Create reviews
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['movie_title']
    ordering_fields = ['rating', 'created_date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Retrieve, Update, Delete reviews
class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

from rest_framework import generics, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer

# Only owner can edit/delete
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

# List and Create reviews
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['movie_title']
    ordering_fields = ['rating', 'created_date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Retrieve, Update, Delete reviews
class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

# Comment list & create
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = Review.objects.get(id=review_id)
        serializer.save(user=self.request.user, review=review)

# Like/unlike a review
from rest_framework.views import APIView
from rest_framework import status

class ReviewLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        review = Review.objects.get(pk=pk)
        user = request.user
        if user in review.likes.all():
            review.likes.remove(user)
            liked = False
        else:
            review.likes.add(user)
            liked = True
        return Response({'liked': liked, 'likes_count': review.likes.count()}, status=status.HTTP_200_OK)
