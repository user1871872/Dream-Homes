from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render,HttpResponse
from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    HotelListingForm,
    LoginForm,
    MessageForm,
)
from .models import HotelListing,Message,CustomUser
import logging

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
