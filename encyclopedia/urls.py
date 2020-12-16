from django.urls import path

from . import views
# app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("new-page", views.new_page, name="new_page"),
    path("<str:entry_name>", views.entry, name="entry"),
]
