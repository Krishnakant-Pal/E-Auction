from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_details, name="listing_details"),
    path("addtowatchlist/<str:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("closebid/<int:listing_id>", views.close_bid, name="close_bid"),
    path("closedlisting/", views.closed_listings,name="closed_listings"),
    path("comment_sent/<int:listing_id>/", views.comment_sent, name="comment_sent"),
]
