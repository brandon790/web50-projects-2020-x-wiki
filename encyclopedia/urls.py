from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name='index'),
    path("wiki/<str:title>", views.wiki, name='wiki'),
    path("newentry", views.newentry, name='newentry'),
    path("editentry", views.editentry, name='editentry'),
    path("randomentry", views.randomentry, name='randomentry'),
    path("search", views.search, name='search')
]
