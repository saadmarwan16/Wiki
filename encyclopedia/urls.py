from django.urls import path

from . import views
# app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("new-page", views.new_page, name="new_page"),
    path("search", views.search, name="search"),
    path("edit-page/<str:filename>", views.edit_page, name="edit_page"),
    path("<str:entry_name>", views.entry, name="entry"),
    # path("wiki/<str:filename>", views.entry, name="entry"),
]
