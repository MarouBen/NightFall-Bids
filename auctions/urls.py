from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings", views.listings, name="listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:pk>/",views.item_view, name="view"),
    path("watchlist", views.watchlist, name="watchlist")
]