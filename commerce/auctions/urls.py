from django.urls import path

from . import views
app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.CreateListing, name="create"),
    path("insert", views.insert, name="insert"),
    path("listing/<int:iduser>", views.listing, name="listing"),
    path("watch/<int:id>", views.watch, name="watch"),
    path("unwatch/<int:id>", views.unwatch, name="unwatch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("Catagories", views.catagories, name="catagories"),
    path("closebid/<int:id>", views.closebid, name="closebid"),
    path("Your Winnings/", views.winnings, name="yourwinnings")


]
