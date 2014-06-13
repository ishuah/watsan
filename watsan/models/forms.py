from django import forms
#from django.forms.widgets import ChoiceField
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User

from watsan.models.users import WatsanUserMeta
from watsan.models.organizations import Organization 
from watsan.models.change_email import NewEmail

class RegisterUserForm(forms.ModelForm):

	email     = forms.EmailField(label='* Email', required=True)
	password1 = forms.CharField(label='* Password', widget=forms.PasswordInput, required=True)
	password2 = forms.CharField(label='* Confirm password', widget=forms.PasswordInput, required=True)
	

	class Meta:
		model = User
		fields = ('first_name', 'last_name')

	def clean_password(self):
		if self.is_valid():
			password1 = self.cleaned_data.get("password1")
			password2 = self.cleaned_data.get("password2")
			if password1 and password2 and password1 != password2:
				self._errors["password1"] = self.error_class([u"Your passwords didn't match!"])
				return False

			return password2
		else:
			return False 
	

	def save(self, commit=True):
		user = super(RegisterUserForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		print RegisterUserForm
		if commit:
			user.save()
		return user


	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data.get("email")
			if User.objects.filter(email=email).exists():
				self._errors["email"] = self.error_class([u"Email is already registered."])
				return False
			return email
		else:
			return False

class OrganizationForm(forms.ModelForm):
	ORG_TYPE_CHOICES = (('CBO', 'CBO'), 
				('NGO', 'NGO'), 
				('school', 'School'), 
				('private', 'Private'))

	org_type = forms.ChoiceField(widget=forms.RadioSelect, required=True, label='* What type of organization do you work for?', choices=ORG_TYPE_CHOICES)
	name = forms.CharField(label='* Organization name', max_length=50, required=True)

	class Meta():
		model = Organization
		fields = ('org_type', 'name')


class UserMetaForm(forms.ModelForm):
	Q1_CHOICES = (('KDI', 'KDI'),
				   ('Spatial Collective', 'Spatial Collective'),
				   ('NCWSC', 'NCWSC'),
				   ('Radio', 'Radio'),
				   ('Billboard', 'Billboard'),
				   ('Friend', 'Friend'),
				   ('CBO', 'CBO'),
				   ('Internet', 'Internet'),
				   ('Other', 'Other')
			)

	Q2_CHOICES = (
				('To build a new sanitation facility', 'To build a new sanitation facility'),
				('To build a new water point', 'To build a new water point'),
				('To connect an existing Sanitation Facility', 'To connect an existing Sanitation Facility'),
				('To connect an existing Water point', 'To connect an existing Water point'),
				('Just looking', 'Just looking'),
				('Other', 'Other')
		)

	question_1 = forms.ChoiceField(widget=forms.RadioSelect, label='How did you hear about the WATSAN portal?', required=False, choices=Q1_CHOICES)
	question_2 = forms.ChoiceField(widget=forms.RadioSelect, label='What are you using the portal for?', required=False, choices=Q2_CHOICES)

	class Meta():
		model = WatsanUserMeta
		fields = ('question_1', 'question_2')

class AddUserForm(forms.ModelForm):
	email = forms.EmailField(required=True)

	class Meta():
		model = User
		fields = ('email',)

	def save(self, commit=True):
		user = super(AddUserForm, self).save(commit=False)
		if commit:
			user.save()
		return user

	def clean_email2(self):
		if self.is_valid():
			email = self.cleaned_data.get("email")
			if User.objects.filter(email=email).exists():
				self._errors["email"] = self.error_class([u"Email is already registered."])
				return False
			return email
		else:
			return False

class EditUserNameForm(forms.ModelForm):
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)

	class Meta():
		model = User
		fields = ('first_name', 'last_name',)

class ChangeUserEmailForm(forms.ModelForm):
	email = forms.EmailField(required=True)

	class Meta():
		model = NewEmail
		fields = ('email',)
