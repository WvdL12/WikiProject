from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("newpage", views.newpage, name="newpage"),
    path("randompage", views.randompage, name="randompage")
]