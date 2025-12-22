
from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = [
            'id',
            'movie_title',
            'content',
            'rating',
            'user',
            'created_at'
        ]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_movie_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Movie title is required.")
        return value

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Review content is required.")
        return value
    
def validate_rating(self, value):
    if value < 0 or value > 5:
     raise serializers.ValidationError("Rating must be between 0 and 5.")
    return round(value, 1)

def create(self, validated_data):
    validated_data['user'] = self.context['request'].user
    return super().create(validated_data)





