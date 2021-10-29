from rest_framework import serializers
from django.contrib.auth import get_user_model

from account.models import UserFollowing
from .models import Song, Comment, Like, Rating, Genre, Favourite


User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', )


class SongSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.email')

    class Meta:
        model = Song
        fields = ('artist', 'title', 'genre', 'image', 'song_file', 'uploader')

    def create(self, validated_data):
        request = self.context.get('request')
        uploader = request.user
        song = Song.objects.create(uploader=uploader, **validated_data)
        return song

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')

        total_rate = 0
        for rate in instance.ratings.all():
            total_rate += int(rate.ratings)
            representation['rating'] = total_rate / instance.ratings.all().count()
        if action == 'retrieve':
            representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
            representation['likes'] = LikeSerializer(instance.likes.all(), many=True).data
        elif action == 'list':
            representation['comments'] = instance.comments.count()
            representation['likes_count'] = instance.likes.filter(likes=True).count()
        # representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = ('author', 'comment', 'created_at', )

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        commented = Comment.objects.create(author=author, **validated_data)
        return commented


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Like
        fields = ('author', 'likes', )

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        song = validated_data.get('song')
        like = Like.objects.get_or_create(author=author, song=song)[0]
        if like.likes:
            like.likes = False
        else:
            like.likes = True
        like.save()

        return like


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        song = validated_data.get('song')
        rating = Rating.objects.get_or_create(author=author, song=song)[0]
        rating.ratings = validated_data['ratings']
        rating.save()
        return rating


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['song'] = instance.song.title
        return representation

