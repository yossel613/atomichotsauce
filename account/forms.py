from xml.dom import NoModificationAllowedErr
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].required = True
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use')
        
        if len(email) >= 99:
            raise forms.ValidationError('Your email is too long')

        return email
    
    
class LoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
    
    
class UpdateUserForm(forms.ModelForm):
    password = None
    
    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].required = True
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This username is already in use')
        
        if len(username) >= 150:
            raise forms.ValidationError('Your username is too long')

        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use')
        
        if len(email) >= 99:
            raise forms.ValidationError('Your email is too long')

        return email
        
    
        
   