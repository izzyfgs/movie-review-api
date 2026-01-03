from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  

    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'user', 'created_date']

from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(max_digits=2, decimal_places=1, min_value=1.0, max_value=5.0)

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie_title', 'review_content', 'rating', 'created_date']
        read_only_fields = ['user', 'created_date']


from rest_framework import serializers
from .models import Review, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_date']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True) 

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie_title', 'review_content', 'rating', 'created_date', 'likes_count', 'comments']

    def get_likes_count(self, obj):
        return obj.likes.count()

from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()  

    class Meta:
        model = Review
        fields = [
            "id",
            "movie_title",
            "review_content",
            "rating",
            "created_date",
            "likes_count",
            "comments",  
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return obj.comments.count()  

