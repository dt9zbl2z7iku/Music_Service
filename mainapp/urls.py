from django.urls import path

from mainapp.views import SubscriptionView, MyPlaylistsView, HomeView, ListenTrackView, PublicPlaylistsListView, PlaylistUpdateView, PlaylistCreateView, PlaylistDeleteView, RecommendationsView, NotFoundView, MyAudioListView, TrackUploadView, PlaylistDetailView, ArtistListView, ArtistDetailView, ArtistCreateView, ArtistUpdateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('genre_filter/<int:genre_id>/', HomeView.as_view(), name='genre_filter'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('listen_track/', ListenTrackView.as_view(), name='listen_track'),
    path('playlists/', PublicPlaylistsListView.as_view(), name='playlists'),
    path('my_playlists/', MyPlaylistsView.as_view(), name='my_playlists'),
    path('update_playlist/<int:pk>', PlaylistUpdateView.as_view(), name='edit_playlist'),
    path('delete_playlist/<int:pk>', PlaylistDeleteView.as_view(), name='delete_playlist'),
    path('create_playlist/', PlaylistCreateView.as_view(), name='add_playlist'),
    path('recommendation/', RecommendationsView.as_view(), name='recommendations'),
    path('my-audio/', MyAudioListView.as_view(), name='my_audio'),
    path('upload-track/', TrackUploadView.as_view(), name='track_upload'),
    path('playlist/<int:id>/', PlaylistDetailView.as_view(), name='playlist_detail'),
    path('artists/', ArtistListView.as_view(), name='artist_list'),
    path('artists/<int:pk>/', ArtistDetailView.as_view(), name='artist_detail'),
    path('artists/add/', ArtistCreateView.as_view(), name='add_artist'),
    path('artists/edit/<int:pk>/', ArtistUpdateView.as_view(), name='edit_artist'),
]
