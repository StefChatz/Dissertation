from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account
from account.models import MyModel

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

	class Meta:
		model = Account
		fields = ("email", "username", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")



class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email', 'username')

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use.' % email)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError('Username "%s" is already in use.' % username)


# CATEGORY_CHOICES = [
# 	('GAMES', 'Games'),
# 	('SOCIAL', 'Social Networking'),
# 	('MUSIC', 'Music'),
# 	('NEWS', 'Breaking News'),
# 	('FINANCE', 'Finance'),
# 	('MOVIES', 'Movies'),
# 	('SPORTS', 'Sports'),
# 	('TRAVEL', 'Travel'),
# 	('AUTOMOTIVE', 'Automotive'),
# 	('LEISURE', 'Leisure')
# ]
#
# class ChoicesForm(forms.Form):
#
# 	def __init__(self, *args, **kargs):
# 		super(UserForm, self).__init__(*args, **kargs)
#
# category_field = forms.ChoiceField(choices = CATEGORY_CHOICES)
class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['color']
