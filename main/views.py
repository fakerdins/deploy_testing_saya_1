from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework import filters as rest_filters
from rest_framework.permissions import IsAuthenticated

from .models import Post, Image, Comment, Like, Rating
from .serializers import PostSerializer, ImageSerializer, CommentSerializer, LikeSerializer, RatingSerializer
from .permissions import IsAuthenticatedAndOwner


class PermissionsMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = (IsAuthenticated, )
        elif self.action in ('update', 'partial_update', 'destroy'):
            permissions = (IsAuthenticatedAndOwner, )
        else:
            permissions = []
        return [permission() for permission in permissions]


class PostViewset(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter
    ]
    filterset_fields = ['id', 'likes']
    search_fields = ['author', 'title', 'text']

    serializer_class = PostSerializer


class LikeViewset(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class ImageViewset(viewsets.ModelViewSet):

    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CommentViewset(PermissionsMixin, viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RatingViewset(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
