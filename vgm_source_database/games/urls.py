from django.urls import path

from .views import (
    GameCreateView,
    GameDeleteView,
    GameDetailView,
    GameListView,
    GameUpdateView,
    GameTagCreateView,
    GameTagDeleteView,
    GameTagDetailView,
    GameTagListView,
    GameTagUpdateView,
)

app_name = "games"
urlpatterns = [
    # Games
    path("", GameListView.as_view(), name="game_list"),
    path("<int:pk>/", GameDetailView.as_view(), name="game_detail"),
    path("create/", GameCreateView.as_view(), name="game_create"),
    path("<int:pk>/update/", GameUpdateView.as_view(), name="game_update"),
    path("<int:pk>/delete/", GameDeleteView.as_view(), name="game_delete"),
    # Game Tags
    path("tags/", GameTagListView.as_view(), name="gametag_list"),
    path("tags/create/", GameTagCreateView.as_view(), name="gametag_create"),
    path("tags/<slug:slug>/", GameTagDetailView.as_view(), name="gametag_detail"),
    path("tags/<slug:slug>/update/", GameTagUpdateView.as_view(), name="gametag_update"),
    path("tags/<slug:slug>/delete/", GameTagDeleteView.as_view(), name="gametag_delete"),
]
