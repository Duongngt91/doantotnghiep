from django import forms
from .models import Nguoidung
from django.contrib.auth.forms import UserCreationForm


class dangkyform (UserCreationForm ):
  class Meta:
    model = Nguoidung
    fields = ['username','phone','email','address','password1','password2']
