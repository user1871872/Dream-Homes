from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include

from myapp.views import MessageDetailAPIView,MessageListCreateAPIView


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
    path('chats/', views.chats, name='chats'),
    path('api/messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('api/message/<int:pk>/', MessageDetailAPIView.as_view(), name='message-detail'),
    path('api/messages/<int:user_id>/', views.get_user_messages, name='get_user_messages'),
    path('edit-message/<int:message_id>/', views.edit_message, name='edit_message'),
    path('unsend-message/<int:message_id>/', views.unsend_message, name='unsend_message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
