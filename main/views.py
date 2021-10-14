from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework import filters as rest_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import csv
from django.http import HttpResponse

from .models import Post, Image, Comment, Like, Rating
from .serializers import PostSerializer, ImageSerializer, CommentSerializer, LikeSerializer, RatingSerializer
from .permissions import IsAuthenticatedAndOwner
from .parser import main


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


class PostFavouriteView(APIView):

    def post(self, request):
        print(request.data)
        post = get_object_or_404(Post, id=request.data.get('post'))
        if request.user not in post.favourite.all():
            post.favourite.add(request.user)
            return Response({'detail': 'added to favourites'}, status=status.HTTP_200_OK)
        return Response({'detail': 'That post already in favourites'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        post = get_object_or_404(Post, id=request.data.get('post'))
        if request.user in post.favourite.all():
            post.favourite.remove(request.user)
            return Response({'detail': 'removed from favourites'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'That post not in your favourites'}, status=status.HTTP_400_BAD_REQUEST)


class ParsingView(APIView):

    def get(self, request):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="data.csv"'},
        )
        list_ = []
        data = open('data.csv')
        list_ = data.read()
        data = csv.writer(response)
        data.writerow([list_])

        return response


