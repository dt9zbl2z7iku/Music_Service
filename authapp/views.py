import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, FormView

from authapp.forms import LoginForm
from authapp.models import User
from mainapp.models import ListeningHistory


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        listened_tracks = ListeningHistory.objects.filter(user=request.user, is_hide=False).order_by('-listened_at')[:10]
        return render(
            request, 'authapp/user_profile.html',
            {'listened_tracks': [
                {'id': history.id,
                 'track': history.track
                 } for history in listened_tracks]
            },
        )


@csrf_exempt
def hide_track(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        history_id = data.get('history_id')

        try:
            listening_history = ListeningHistory.objects.get(id=history_id)
            listening_history.is_hide = True
            listening_history.save()
            return redirect('user_profile')
        except ListeningHistory.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No ListeningHistory matches the given query.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'authapp/user_profile.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = self.request.user
        user.phone = self.request.POST.get('phone')
        if 'avatar' in self.request.FILES:
            user.avatar = self.request.FILES['avatar']
        user.save()
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'authapp/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('user_profile')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        print(user)
        if user is not None and user.is_active:
            login(self.request, user)
            return redirect('home')
        else:
            # Обработка ошибки аутентификации
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Обработка ошибки аутентификации
        return render(self.request, self.template_name, {'form': form})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class RegisterFormView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # Обработка ошибки регистрации
        print(form.error_messages)
        return super().form_invalid(form)


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('home'))
