from django.urls import path
from .views import CreateMovieView, AllMovieListView, DeleteMovieView

urlpatterns = [
    path("create/",CreateMovieView.as_view(),name="create"),
    path("shows/",AllMovieListView.as_view(), name="shows"),
    path("delete/<str:pk>",DeleteMovieView.as_view(),name="delete"),
]