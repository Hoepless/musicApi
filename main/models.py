from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Genre(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return str(self.name)


class Song(models.Model):
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs', null=True)
    image = models.ImageField(upload_to='song_cover')
    song_file = models.FileField(upload_to='songs')
    lyrics = models.TextField(blank=True, null=True)
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='songs')

    def __str__(self):
        return str(self.artist) + " | " + str(self.title)


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', null=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='likes', blank=True)
    likes = models.BooleanField(default=False)

    def __str__(self):
        return str(self.likes)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)
    comment = models.TextField()
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment)


class Favourite(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favourites')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    favourite = models.BooleanField(default=False)

    def __str__(self):
        return str(self.favourite)


class Rating(models.Model):
    RATE = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5")
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', null=True)
    ratings = models.CharField(choices=RATE, max_length=1, default=0)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return f"{self.song} | {self.ratings}"

