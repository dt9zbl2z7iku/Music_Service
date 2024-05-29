from django import forms

from mainapp.models import Playlist, Track, Artist


class TrackUploadForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artist', 'genres', 'cover_image', 'audio_file', 'is_popular']


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'cover', 'is_private', 'description']
        labels = {
            'name': 'Название',
            'cover': 'Обложка',
            'is_private': 'Приватный плейлист',
            'description': 'Описание',
        }


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'bio', 'image']
