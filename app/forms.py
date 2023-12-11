from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']    

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['rubric', 'title', 'content', 'price', 'contact', 'image']

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'price', 'contact', 'image')
    
        
        
        