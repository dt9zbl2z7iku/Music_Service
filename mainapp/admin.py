from django.contrib import admin
from .models import Artist, Genre, Track, Playlist, Subscription

admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Track)
admin.site.register(Playlist)
admin.site.register(Subscription)
