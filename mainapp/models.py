from django.db import models
from django.utils import timezone

from authapp.models import User


class Artist(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='img/', blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Track(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, related_name='tracks', on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre, related_name='tracks')
    cover_image = models.ImageField(upload_to='static/img/', blank=True, null=True, default='static/img/default-cover.png')
    audio_file = models.FileField(upload_to='static/audio/')
    is_popular = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='tracks', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.artist.name}"


class ListeningHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(default=timezone.now)
    is_hide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} listened to {self.track.title}"


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='playlists', on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to='static/img/', blank=True, default='static/img/default-cover.png')
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('FREE', 'Free'),
        ('PREMIUM', 'Premium'),
        ('PRO', 'Pro'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_type = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_CHOICES,
        default='FREE',
    )
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.subscription_type}"
