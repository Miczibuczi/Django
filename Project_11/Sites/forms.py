from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Post

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise ValidationError("Posswords do not match")

        username = cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already taken.")

        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already taken")
        return cleaned_data
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]