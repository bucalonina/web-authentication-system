#* Marko Dasic 2022/0731

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


####################################### Marko ###########################################################################################

# register form
class MyUserCreationForm(UserCreationForm):
    gender = forms.ChoiceField(choices=((True, 'Male'), (False, 'Female')), widget=forms.RadioSelect)
    hobbies = forms.ModelMultipleChoiceField(queryset=Hobby.objects.all(), widget=forms.CheckboxSelectMultiple)

    hobbies.label_from_instance = lambda obj: f"{obj.name} - {obj.description}"

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'gender', 'first_name', 'last_name', 'age', 'city', 'state', 'picture', 'bio', 'hobbies']

# rating forms
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'description']

# update user data form
class UpdateUserForm(UserCreationForm):
    gender = forms.ChoiceField(choices=((True, 'Male'), (False, 'Female')), widget=forms.RadioSelect)
    hobbies = forms.ModelMultipleChoiceField(queryset=Hobby.objects.all(), widget=forms.CheckboxSelectMultiple)

    hobbies.label_from_instance = lambda obj: f"{obj.name} - {obj.description}"

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'gender', 'first_name', 'last_name', 'age', 'city', 'state', 'picture', 'bio', 'hobbies']


####################################### Pavle ###########################################################################################



####################################### Vladana ###########################################################################################

# Report
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']

####################################### Nina ###########################################################################################
