from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/create", views.create_listing, name="create_listing"),
    path("listing/<str:listing_title>", views.listing_details, name="listing_details"),
    path("addtowatchlist/<str:listing_title>", views.add_to_watchlist, name="add_to_watchlist"),
]
