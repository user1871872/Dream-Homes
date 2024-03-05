from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import User

from .models import CustomUser, HotelListing


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "user_type",
            "email",
            "phone_number",
            "birth_date",
        )
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Exclude the profilepic field
            self.fields.pop("profile_picture")


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "profile_picture",
            "email",
            "phone_number",
            "birth_date",
        )
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude the password field
        self.fields.pop("password")


class HotelListingForm(forms.ModelForm):
    class Meta:
        model = HotelListing
        fields = [
            "title",
            "location",
            "description",
            "price",
            "available_for_sale",
            "available_for_rent",
            "contact_email",
            "image",
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(
        choices=(("client", "Client"), ("agent", "Agent"), ("company", "Company"))
    )
