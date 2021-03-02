from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("claim", views.claim, name="claim"),
    path("tracks/<int:track_id>", views.track, name="track"),
    path("tracks/<int:track_id>/comment", views.comment, name="comment"),
    path("book/<int:book_id>", views.book, name="book"),
    path("favorite", views.favorite, name="favorite"),
    path("writer/<int:writer_id>", views.writer, name="writer"),
    path("user/<int:user_id>", views.profile, name="profile"),
    path("requested", views.requested, name="requested"),
    path("join", views.join_request, name="join_request"),
    

        # API Routes
    path("like/<int:track_id>", views.like, name="like")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)