from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.custom_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("userprofile/", views.updateprofiles, name="userprofile"),
    path("approval/", views.approval, name="approval"),
    path("houselist/", views.houselisting, name="houselist"),
    path('chat/', views.chat_room, name='chat_room'),
    path('chat/<int:receiver_id>/', views.chat_room, name='chat_room_with_receiver'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
