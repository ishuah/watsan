from django import forms
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.forms.widgets import RadioSelect, HiddenInput, PasswordInput

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    next = models.CharField(default="/", max_length=100)

    number = models.CharField(max_length=20, blank=True)
    secondary_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(blank=True, choices=(('male', 'Male'), ('female', 'Female')), max_length=10)
    picture = models.ImageField(upload_to="UserAvatars", blank=True, null=True)
    has_mpesa = models.NullBooleanField()
    organization = models.CharField(max_length=255, blank=True)

    confirmation_code = models.CharField(max_length=20 ,blank=True, null=True)

    class Meta:
        app_label = 'user_control'
        db_table = 'user_control_userprofile'
    
    def __unicode__(self):
        return self.user.username+"'s profile"

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=30, required=True)

    old_password = forms.CharField(max_length=30, required=False, widget=PasswordInput())
    new_password = forms.CharField(max_length=30, required=False, widget=PasswordInput())
    new_password_again = forms.CharField(max_length=30, required=False, widget=PasswordInput())
    
    def clean(self):
        cleaned_data = super(UserEditForm, self).clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        new_password2 = cleaned_data.get("new_password_again")
        if old_password and new_password:
            if not self.instance.check_password(old_password):
                self._errors["old_password"] = self.error_class([u"Incorrect Password!"])
            elif not new_password2:
                self._errors["new_password_again"] = self.error_class([u"Must enter new password twice"])
            elif not new_password == new_password2:
                self._errors["new_password"] = self.error_class([u"Your new passwords didn't match!"])
        return cleaned_data
    
    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','username', 'old_password','new_password','new_password_again')

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    number = forms.CharField(max_length=20, required=False)
    secondary_number = forms.CharField(max_length=20, required=False)
    gender = forms.CharField(required=False, widget=forms.RadioSelect(choices=(('male', 'Male'), ('female', 'Female'))), max_length=10)
    picture = forms.ImageField(required=False)
    has_mpesa = forms.NullBooleanField(required=True, widget=RadioSelect(choices=((None, 'Unknown'), (True, 'Yes'), (False, 'No'))))
    organization = forms.CharField(required=False, max_length=255)
    
    class Meta:
        model = UserProfile
        fields = ('email','number','secondary_number','gender','picture','has_mpesa')
        exclude = ('user', 'next')
        
class AddMemberForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=False)
    number = forms.CharField(max_length=20, required=False)
    can_export_data = forms.BooleanField(required=False)
    is_admin = forms.BooleanField(help_text="This will enable this user to add and remove users, and make other major changes to your collective (including exporting data)", required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'number')

class NewUserForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField()
    password1 = forms.CharField(label='Password',max_length=30, widget=PasswordInput())
    organization = forms.CharField(label='Organization', max_length=30, required=False)

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                self._errors["email"] = self.error_class([u"Email is already registered."])
                return False
            return email
        else:
            return False

    class Meta:
        model = User
        fields = ('username', 'email', 'password1','organization')