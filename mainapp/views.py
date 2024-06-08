import json
import random
from datetime import timedelta, date

from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, TemplateView, DetailView

from mainapp.forms import TrackUploadForm, ArtistForm
from mainapp.mixins import SubscriptionRequiredMixin
from mainapp.models import Track, Subscription, ListeningHistory, Playlist, Genre, Artist


class HomeView(ListView):
    model = Track
    template_name = 'mainapp/index.html'
    context_object_name = 'popular_tracks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = True
        context['genres'] = Genre.objects.all()
        try:
            context['day_track'] = Track.objects.get(id=2)
        except Exception as e:
            context['day_track'] = None
        return context

    def get_queryset(self):
        queryset = Track.objects.filter(is_popular=True)
        genre_id = self.kwargs.get('genre_id')
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)
        else:
            queryset = queryset.all()
        return queryset


class SubscriptionView(View):
    template_name = 'mainapp/subscription.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_anonymous:
            subscription, created = Subscription.objects.get_or_create(user=user)
            return render(request, self.template_name, {'subscription': subscription})
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return redirect('login')

        # Получаем или создаем подписку пользователя
        subscription, created = Subscription.objects.get_or_create(user=user)

        # Обновляем тип подписки и дату окончания
        subscription_type = request.POST.get('subscription_type')
        subscription.subscription_type = subscription_type
        if subscription_type == 'FREE':
            subscription.expiry_date = None
        else:
            subscription.expiry_date = now().date() + timedelta(days=30)
        subscription.save()

        return redirect('subscription')


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ListenTrackView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            track_id = data.get('track_id')
            track = get_object_or_404(Track, id=track_id)
            ListeningHistory.objects.create(user=request.user, track=track)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


class PublicPlaylistsListView(ListView):
    model = Playlist
    template_name = 'mainapp/playlists.html'
    context_object_name = 'public_playlists'

    def get_queryset(self):
        return Playlist.objects.filter(is_private=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PlaylistUpdateView(UpdateView):
    model = Playlist
    fields = ['name', 'is_private']
    template_name = 'mainapp/playlist_update.html'
    success_url = reverse_lazy('my_playlists')


class PlaylistDeleteView(DeleteView):
    model = Playlist
    success_url = reverse_lazy('my_playlists')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        playlist = get_object_or_404(Playlist, pk=kwargs['pk'])
        playlist.delete()
        return redirect(self.success_url)


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'is_private', 'cover']

    existing_tracks = forms.ModelMultipleChoiceField(
        queryset=Track.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Выберите существующие треки"
    )


class ArtistListView(ListView):
    model = Artist
    template_name = 'mainapp/artist_list.html'
    context_object_name = 'artists'


class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'mainapp/artist_detail.html'
    context_object_name = 'artist'


class ArtistCreateView(LoginRequiredMixin, CreateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'mainapp/artist_form.html'
    success_url = reverse_lazy('artist_list')
    login_url = reverse_lazy('login')


class ArtistUpdateView(LoginRequiredMixin, UpdateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'mainapp/artist_form.html'
    context_object_name = 'artist'
    success_url = reverse_lazy('artist_list')
    login_url = reverse_lazy('login')


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'mainapp/playlist_create.html'
    success_url = reverse_lazy('my_playlists')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RecommendationsView(View):
    template_name = 'mainapp/recommendations.html'
    num_recommendations = 10

    def get(self, request, *args, **kwargs):
        try:
            genre = Genre.objects.get(id=5)
            tracks = list(genre.tracks.all())
            print(tracks)
        except Genre.DoesNotExist:
            tracks = list(Track.objects.all())

        if len(tracks) > self.num_recommendations:
            recommended_tracks = random.sample(tracks, self.num_recommendations)
        else:
            recommended_tracks = tracks

        context = {
            'recommended_tracks': recommended_tracks
        }
        return render(request, self.template_name, context)


class NotFoundView(TemplateView):
    template_name = '404_template.html'


class MyAudioListView(SubscriptionRequiredMixin, ListView):
    model = Track
    template_name = 'mainapp/my_audio.html'
    context_object_name = 'tracks'

    def get_queryset(self):
        return Track.objects.filter(owner=self.request.user.id)


class TrackUploadView(CreateView):
    model = Track
    form_class = TrackUploadForm
    template_name = 'mainapp/track_upload.html'
    success_url = reverse_lazy('my_audio')

    def form_valid(self, form):
        track = form.save(commit=False)
        track.owner_id = self.request.user.id
        track.save()
        form.save_m2m()
        return super().form_valid(form)


class MyPlaylistsView(ListView):
    model = Playlist
    template_name = 'mainapp/my_playlists.html'
    context_object_name = 'user_playlists'

    def has_active_subscription(self):
        user = self.request.user
        subscription = user.subscription.objects.filter(user_id=self.id, expiry_date__gte=date.today()).first()
        return subscription is not None

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)


class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = 'mainapp/playlist_detail.html'
    context_object_name = 'playlist'

    def get_object(self):
        return get_object_or_404(Playlist, id=self.kwargs['id'])
