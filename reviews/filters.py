import django_filters
from .models import Review

class ReviewFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter(field_name='rating', lookup_expr='exact')

    class Meta:
        model = Review
        fields = ['rating', 'movie_title']
