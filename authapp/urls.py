from django.contrib.auth.views import LogoutView
from django.urls import path

from authapp.views import UserProfileUpdateView, RegisterFormView, ProfileView, hide_track, CustomLogoutView, LoginView

urlpatterns = [
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile_update/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('profile/', ProfileView.as_view(), name='user_profile'),
    path('hide_track/', hide_track, name='hide_track'),
    path('edit_profile/', UserProfileUpdateView.as_view(), name='edit_profile'),
]
