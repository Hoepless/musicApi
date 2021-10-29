from django_filters import rest_framework as filters
from rest_framework import viewsets, status, generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
import csv
from rest_framework.views import APIView


from .models import *
from .serializers import SongSerializer, GenreSerializer, CommentSerializer, \
    LikeSerializer, RatingSerializer, FavouriteSerializer
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


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class SongViewSet(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = ['title']
    search_fields = ['artist', 'title']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        context['request'] = self.request
        return context

    @action(detail=False, methods=['get'])
    def favourites(self, request):
        queryset = Favourite.objects.all()
        queryset = queryset.filter(author=request.user, favourite=True)
        serializer = FavouriteSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def favourite(self, request, pk=None):
        song = self.get_object()
        obj, created = Favourite.objects.get_or_create(author=request.user, song=song)
        if not created:
            obj.favourite = not obj.favourite
            obj.save()
        if obj.favourite:
            favourites = 'added to favourites!'
        else:
            favourites = 'removed from favourites'
        # favourites = 'added to favourites!' if obj.favourite else 'removed to favorites'

        return Response(f'Successfully {favourites} !', status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def recommendations(self, request, pk=None):
        queryset = Song.objects.all()
        object = self.get_object()
        queryset = queryset.filter(uploader=request.user, genre=object.genre)
        serializer = SongSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class LikeViewset(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class CommentViewset(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RatingViewset(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class ParsingView(APIView):

    def get(self, request):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="data.csv"'},
        )
        list_ = []
        data = open('./data.csv')
        list_ = data.read()
        data = csv.writer(response)
        data.writerow([list_])

        return response