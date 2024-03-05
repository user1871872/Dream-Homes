from django.contrib import admin

from .models import CustomUser, HotelListing

admin.site.register(CustomUser)
admin.site.register(HotelListing)
