from django.urls import path
from .views import ReviewListCreateView, ReviewRetrieveUpdateDestroyView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review-list-create'),
    path('<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),
]
from django.urls import path
from .views import ReviewListCreateView, ReviewRetrieveUpdateDestroyView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review-list-create'),  # /api/reviews/
    path('<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),  # /api/reviews/1/
]

from django.urls import path
from .views import (
    ReviewListCreateView,
    ReviewRetrieveUpdateDestroyView,
    CommentListCreateView,
    ReviewLikeToggleView
)

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review-list-create'),
    path('<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),
    path('<int:review_id>/comments/', CommentListCreateView.as_view(), name='review-comments'),
    path('<int:pk>/like/', ReviewLikeToggleView.as_view(), name='review-like-toggle'),
]
