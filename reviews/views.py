from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from django.db.models import Count
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer


class ReviewFilter(FilterSet):
    rating = NumberFilter(field_name='rating', lookup_expr='exact')

    class Meta:
        model = Review
        fields = ['movie_title', 'rating']

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReviewFilter   
    search_fields = ['movie_title']  
    ordering_fields = ['rating', 'created_date', 'likes_count', 'comments_count']
    template_name = None                

    def get_queryset(self):
        return Review.objects.annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments')
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments')
        )
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

from rest_framework.authentication import TokenAuthentication
class ReviewLikeToggleView(APIView):
    authentication_classes = [TokenAuthentication]  
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
from django.shortcuts import render
from django.http import HttpResponse

def api_home(request):
    return HttpResponse("""
        <h1>Welcome to the Movie Review API</h1>
        <ul>
            <li><a href="/login/">Login (Token Auth)</a></li>
            <li><a href="/register/">Register</a></li>
            <li><a href="/api/reviews/">Reviews Endpoint</a></li>
            <li><a href="/admin/">Admin</a></li>
        </ul>
    """)