from django.contrib import admin
from main.models import Genre, Song, Comment, Like, Favourite, Rating

admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Favourite)

