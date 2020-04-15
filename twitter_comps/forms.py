from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm

class CreateUserForm(UserCreationForm):

	class Meta:
		model = User
		fields = ('username', 'email', "password1", "password2")

class ProfileEditForm(ModelForm):
	class Meta:
		model = Profile
		fields = (
			"first_name",
			"last_name",
			"description",
			"profile_picture",
					)