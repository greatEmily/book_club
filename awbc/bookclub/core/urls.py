from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("poll/<int:poll_id>/vote/<int:option_id>/", views.vote, name="vote"),
    path("signup/", views.signup, name="signup"),
    path("my-profile/", views.my_profile, name="my_profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
]
