from django import forms
from app import models


class registerClub(forms.ModelForm):
    class Meta:
        model = models.Club
        fields = ("id", "name", "address", "contact", "payment", "discount", "balance",)
