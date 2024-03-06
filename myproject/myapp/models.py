from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    CLIENT = "Client"
    AGENT = "Agent"
    COMPANY = "Company"

    USER_TYPE_CHOICES = [
        (CLIENT, "Client"),
        (AGENT, "Agent"),
        (COMPANY, "Company"),
    ]

    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    profile_picture = models.ImageField(
        upload_to="profile_pictures",
        null=True,
        blank=True,
        default="image/default.png",
    )
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)


class HotelListing(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_for_sale = models.BooleanField(default=False)
    available_for_rent = models.BooleanField(default=False)
    contact_email = models.EmailField()
    image = models.ImageField(
        upload_to="house_list",
        null=True,
        blank=True,
        default="image/default.png",
    )

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
