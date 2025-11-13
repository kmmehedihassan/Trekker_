from rest_framework import serializers
from .models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for blog categories"""
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_posts_count(self, obj):
        """Get number of posts in this category"""
        return obj.posts.filter(is_published=True).count()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for blog comments"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'content', 'parent',
                  'replies', 'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_replies(self, obj):
        """Get all replies to this comment"""
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_approved=True), many=True).data
        return []


class PostListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for post listings"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    categories_list = CategorySerializer(source='categories', many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'title', 'slug', 'excerpt', 'featured_image',
                  'categories_list', 'likes_count', 'comments_count', 'views_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual post view"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)
    categories_list = CategorySerializer(source='categories', many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'author_email', 'title', 'slug', 'body', 'excerpt',
                  'featured_image', 'media_url', 'categories_list', 'likes_count', 'is_liked_by_user',
                  'comments_count', 'comments', 'views_count', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'views_count']

    def get_is_liked_by_user(self, obj):
        """Check if the current user has liked this post"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating posts"""
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'excerpt', 'featured_image', 'media_url',
                  'categories', 'is_published']

    def validate_slug(self, value):
        """Ensure slug is unique"""
        instance = getattr(self, 'instance', None)
        if instance and instance.slug == value:
            return value

        if Post.objects.filter(slug=value).exists():
            raise serializers.ValidationError("A post with this slug already exists.")

        return value
