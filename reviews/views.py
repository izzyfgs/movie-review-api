from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from django.db.models import Count
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer


# Custom FilterSet for browsable API input fields
class ReviewFilter(FilterSet):
    rating = NumberFilter(field_name='rating', lookup_expr='exact')

    class Meta:
        model = Review
        fields = ['movie_title', 'rating']


# Permission: only owner can edit/delete
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


# List and create reviews
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReviewFilter      # <-- custom filter for rating input
    search_fields = ['movie_title']     # search bar for movie title
    ordering_fields = ['rating', 'created_date', 'likes_count', 'comments_count']
    template_name = None                 # avoids TemplateDoesNotExist error

    def get_queryset(self):
        return Review.objects.annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments')
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Retrieve, update, delete a review
class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments')
        )


# List and create comments for a review
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = generics.get_object_or_404(Review, id=review_id)
        serializer.save(user=self.request.user, review=review)


# Like/unlike a review
class ReviewLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        review = generics.get_object_or_404(Review, pk=pk)
        user = request.user
        if user in review.likes.all():
            review.likes.remove(user)
            liked = False
        else:
            review.likes.add(user)
            liked = True
        return Response(
            {'liked': liked, 'likes_count': review.likes.count()},
            status=status.HTTP_200_OK
        )
