from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("demo/items/", views.item_list, name="item_list"),
    path("demo/items/add/", views.item_add, name="item_add"),
    path("demo/contact/", views.contact, name="contact"),
    path("demo/dashboard/", views.dashboard, name="dashboard"),
]
