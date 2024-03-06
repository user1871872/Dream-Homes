from django.contrib import admin

from .models import CustomUser, HotelListing,Message

admin.site.register(CustomUser)
admin.site.register(HotelListing)
admin.site.register(Message)
