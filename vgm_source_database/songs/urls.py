from django.urls import path

from .views import (
    PersonCreateView,
    PersonDeleteView,
    PersonDetailView,
    PersonListView,
    PersonUpdateView,
    SongCreateView,
    SongDeleteView,
    SongDetailView,
    SongListView,
    SongUpdateView,
)

app_name = "songs"
urlpatterns = [
    # Songs
    path("", SongListView.as_view(), name="song_list"),
    path("<int:pk>/", SongDetailView.as_view(), name="song_detail"),
    path("create/", SongCreateView.as_view(), name="song_create"),
    path("<int:pk>/update/", SongUpdateView.as_view(), name="song_update"),
    path("<int:pk>/delete/", SongDeleteView.as_view(), name="song_delete"),
    # People
    path("people/", PersonListView.as_view(), name="person_list"),
    path("people/<int:pk>/", PersonDetailView.as_view(), name="person_detail"),
    path("people/create/", PersonCreateView.as_view(), name="person_create"),
    path("people/<int:pk>/update/", PersonUpdateView.as_view(), name="person_update"),
    path("people/<int:pk>/delete/", PersonDeleteView.as_view(), name="person_delete"),
]
