from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import Category, Post, Comment
from .serializers import (
    CategorySerializer, PostListSerializer,
    PostDetailSerializer, PostCreateUpdateSerializer,
    CommentSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """Category management viewset"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class PostViewSet(viewsets.ModelViewSet):
    """Blog post management viewset"""
    queryset = Post.objects.filter(is_published=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, slug=None):
        post = self.get_object()
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            message = 'Post unliked'
        else:
            post.likes.add(user)
            message = 'Post liked'
        return Response({'message': message, 'likes_count': post.likes.count()})


class CommentViewSet(viewsets.ModelViewSet):
    """Comment management viewset"""
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
