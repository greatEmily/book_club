from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("poll/<int:poll_id>/vote/<int:option_id>/", views.vote, name="vote"),
    path("signup/", views.signup, name="signup"),
    path("my-profile/", views.my_profile, name="my_profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("polls/", views.poll_list, name="poll_list"),
    path("polls/<int:poll_id>/", views.poll_detail, name="poll_detail"),
    path("past-meetings/", views.past_meetings, name="past_meetings"),
]
