from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("poll/<int:poll_id>/vote/<int:option_id>/", views.vote, name="vote"),
]
