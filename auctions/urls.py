from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("admin", admin.site.urls),
    path("", views.index, name="index"),
    path("listings", views.listings, name="listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:pk>/",views.item_view, name="view"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid", views.bid, name="bid"),
    path("close", views.close, name="close"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("search", views.search, name="search"),
    path("search/category/<str:category>/", views.categories, name="category"),
    path("search/state/<str:state>/", views.state, name="state")
]