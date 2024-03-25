from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render,HttpResponse
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    HotelListingForm,
    LoginForm,
    MessageForm,
)
from .models import HotelListing,Message,CustomUser
import logging
from rest_framework import generics

# Create your views here.
def index(request):
    return render(request, "index.html")


def userprofile(request):
    return render(request, "user_profile.html")


def custom_logout(request):
    logout(request)
    return redirect("home")


def approval(request):
    return render(request, "admin/approval.html")


@login_required
def dashboard(request):
    user = request.user
    return render(request, "dashboard.html", {"user": user})
    # if request.user.user_type == "client":
    #     return render(request, "client_dashboard.html")
    # elif request.user.user_type == "agent":
    #     return render(request, "agent_dashboard.html")
    # elif request.user.user_type == "company":
    #     return render(request, "company_dashboard.html")
    # else:
    #     return render(request, "error.html")
    # account = CustomUserCreationForm.objects.all(account)


def error(request):
    return render(request, "error.html", name="error")


def houselisting(request):
    form = HotelListingForm()
    if request.method == "POST":
        form = HotelListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
        else:
            form = HotelListingForm()
    return render(request, "agent/house_listing.html", {"form": form})


# def houselisting(request):
#     listings = HotelListing.objects.all()
#     return render(request, 'hotel_listings.html', {'listings': listings})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required
def updateprofiles(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, "user_profile.html", {"form": form})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("dashboard")
        else:
            messages.info(request, "Username or Password is Incorrect")
            return redirect("login")
    else:
        return render(request, "login.html")
    

logger = logging.getLogger(__name__)

@login_required
def chat_room(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            receiver_id = form.cleaned_data['receiver_id']
            content = form.cleaned_data['content']
            receiver = CustomUser.objects.get(id=receiver_id)
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return redirect('chat_room')
        else:
            logger.error("Invalid form data: %s", form.errors)
    else:
        form = MessageForm()
    
    all_users = CustomUser.objects.exclude(id=request.user.id)  # Exclude current user from the list
    
    # Fetch messages exchanged between the current user and the selected recipient
    receiver_id = request.GET.get('receiver_id')
    if receiver_id:
        receiver = CustomUser.objects.get(id=receiver_id)
        messages = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user)
    else:
        messages = []
    
    return render(request, 'chat.html', {'form': form, 'all_users': all_users, 'messages': messages})


@login_required
def get_messages(request, receiver_id):
    receiver = CustomUser.objects.get(id=receiver_id)
    messages = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user)
    return render(request, 'chat.html', {'messages': messages, 'receiver_id': receiver_id})

def inboxx(request):
    return render (request, 'inboxx.html')

@login_required
def chats(request):
    # Exclude the currently logged-in user from the list of users
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'chats.html', {'users': users})

from .permissions import IsOwnerOrReadOnly
class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

from django.http import JsonResponse
class MessageDetailAPIView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]
# In your Django app's views.py file

from django.http import JsonResponse
from .models import Message

def get_user_messages(request, user_id):
    # Fetch messages where the sender or receiver is the specified user ID and order them by timestamp
    messages_sent = Message.objects.filter(sender_id=user_id).order_by('timestamp')
    messages_received = Message.objects.filter(receiver_id=user_id).order_by('timestamp')

    # Combine sent and received messages
    messages = messages_sent | messages_received

    # Serialize messages to JSON format
    serialized_messages = []
    for message in messages:
        serialized_message = {
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'timestamp': message.timestamp,
            'sender_profile_picture': None if not message.sender.profile_picture else message.sender.profile_picture.url
        }
        serialized_messages.append(serialized_message)
    
    return JsonResponse(serialized_messages, safe=False)

from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
import logging
logger = logging.getLogger(__name__)

from django.views.decorators.http import require_http_methods
import json

@login_required
@require_http_methods(["PUT"])
def edit_message(request, message_id):
    # Retrieve the message object or return a 404 error if not found
    message = get_object_or_404(Message, pk=message_id)
    
    # Check if the current user is the sender of the message
    if message.sender != request.user:
        logger.error('User %s attempted to edit message %d, which they are not allowed to edit.', request.user, message_id)
        return JsonResponse({'error': 'You are not allowed to edit this message.'}, status=403)
    
    # Check if the content parameter exists in the PUT request data
    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        new_content = body_data.get('content')
    except json.JSONDecodeError:
        new_content = None

    if new_content and new_content.strip():  # Check if content is provided and not empty or whitespace
        # Update the message content
        message.content = new_content
        message.save()
        logger.info('User %s edited message %d successfully.', request.user, message_id)
        return JsonResponse({'success': 'Message edited successfully.'})
    else:
        logger.error('User %s attempted to edit message %d with missing or empty content.', request.user, message_id)
        return JsonResponse({'error': 'Content parameter is missing or empty.'}, status=400)


from django.utils import timezone
# Function to unsend a message
@require_POST
def unsend_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    
    # Check if the message belongs to the current user
    if message.sender != request.user:
        return JsonResponse({'error': 'You are not allowed to unsend this message.'}, status=403)
    
    # Convert the current time to a timezone-aware datetime object
    current_time = timezone.now()
    
    # Check if the message is within the time limit (5 minutes)
    if message.timestamp < current_time - timedelta(minutes=5):
        return JsonResponse({'error': 'The message cannot be unsent after 5 minutes.'}, status=403)
    
    # Delete the message
    message.delete()
    
    return JsonResponse({'success': 'Message unsent successfully.'})

# from django.db.models import Max
# from django.db.models import Q
# def get_user_messages(request, user_id):
#     # Fetch messages where the sender or receiver is the specified user ID
#     messages_sent = Message.objects.filter(sender_id=user_id)
#     messages_received = Message.objects.filter(receiver_id=user_id)

#     # Find the timestamp of the latest message for each user
#     latest_sent_message = messages_sent.aggregate(Max('timestamp'))['timestamp__max']
#     latest_received_message = messages_received.aggregate(Max('timestamp'))['timestamp__max']

#     # Determine the latest message timestamp
#     latest_message_timestamp = max(latest_sent_message, latest_received_message)

#     # Get all users and annotate them with the timestamp of their latest message
#     users = CustomUser.objects.annotate(
#         latest_message=Max('message__timestamp', filter=Q(message__sender=user_id) | Q(message__receiver=user_id))
#     ).order_by('-latest_message')

#     # Serialize users to JSON format
#     serialized_users = []
#     for user in users:
#         serialized_user = {
#             'username': user.username,
#             'latest_message_timestamp': user.latest_message.timestamp() if user.latest_message else None,
#             'profile_picture': user.profile_picture.url if user.profile_picture else None
#         }
#         serialized_users.append(serialized_user)

#     return JsonResponse(serialized_users, safe=False)

# import json

# @csrf_exempt
# def save_event(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         event = Event.objects.create(
#             name=data['eventName'],  # Use 'eventName' instead of 'name'
#             date=data['eventDate'],  # Use 'eventDate' instead of 'date'
#             start_time=data['startTime'],  # Use 'startTime' instead of 'start_time'
#             end_time=data['endTime'],  # Use 'endTime' instead of 'end_time'
#             description=data['eventDescription']  # Use 'eventDescription' instead of 'description'
#         )
#         return JsonResponse({'success': True})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})
    
# def get_events(request, year, month):
#     events = Event.objects.filter(date__year=year, date__month=month)
#     events_data = []
#     for event in events:
#         events_data.append({
#             'name': event.name,
#             'date': event.date.strftime('%Y-%m-%d'),
#             'startTime': event.start_time.strftime('%H:%M'),
#             'endTime': event.end_time.strftime('%H:%M'),
#             'description': event.description
#         })
#     return JsonResponse(events_data, safe=False)
# def events(request):
#    return render(request, 'events.html')

    # if request.method == "POST":
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")
    #     user_type = request.POST.get("user_type")

    #     if username and password and user_type:
    #         user = auth.authenticate(request, username=username, password=password)

    #         if user is not None:
    #             if user.user_type == user_type:
    #                 auth.login(request, user)

    #                 return redirect("dashboard")
    #             else:
    #                 messages.error(request, "Invalid user type or permission denied.")
    #                 return render(request, "login.html")
    #         else:
    #             messages.error(request, "Invalid username or password.")
    #             return render(request, "login.html")
    #     else:
    #         messages.error(request, "All fields are required.")
    #         return render(request, "login.html")
    # else:
    #     return render(request, "login.html")
