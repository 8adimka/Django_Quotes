from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.index, name="index"),
    path("top/", views.top_quotes, name="top"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add/", views.add_quote, name="add"),
    path("like/<int:pk>/", views.like_quote, name="like"),
    path("dislike/<int:pk>/", views.dislike_quote, name="dislike"),
]
