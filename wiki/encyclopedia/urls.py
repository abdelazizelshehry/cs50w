from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.reqpage, name="reqpage"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("random/", views.Random, name="random"),
    path("createcatagory/", views.addcatagory, name="addcatagory"),
    path("catagory/<str:name>", views.catagory, name="topics"),
    path("delete/", views.deletecatagory, name="delete"),
    path("edit/", views.editcatagory, name="edit")

]
