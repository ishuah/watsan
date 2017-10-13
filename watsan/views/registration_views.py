from django.shortcuts import render, redirect
from watsan.models.forms import RegisterUserForm, OrganizationForm, UserMetaForm, AddUserForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission, Group
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from watsan.models import Organization
from watsan.models.users import WatsanUserMeta
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.views import password_reset

def register_org(request):
	if request.method == 'POST':
		org_form = OrganizationForm(request.POST)

		if org_form.is_valid():

			user_form = RegisterUserForm()
			return  render(request, 'registration/register_user.html', { 'user_form': user_form, 'org_form': org_form}) #redirect('/watsan/register/user') 
	else:
		org_form = OrganizationForm()
	return render(request, 'registration/register_org.html', { 'org_form': org_form})

def register_user(request):
	if request.method == 'POST':
		user_form = RegisterUserForm(request.POST)
		org_form = OrganizationForm(request.POST)
		if user_form.is_valid() and user_form.clean_password() and user_form.clean_email():
			meta_form = UserMetaForm()
			return render(request, 'registration/register_final_questions.html', { 'meta_form': meta_form, 'org_form': org_form, 'user_form': user_form }) #redirect('/watsan/register/final')
		
		return render(request, 'registration/register_user.html', { 'user_form': user_form, 'org_form': org_form})
	else:
		user_form = RegisterUserForm()
		return render(request, 'registration/register_user.html', { 'user_form': user_form})

def register_final(request):
	if request.method == 'POST':
		meta_form = UserMetaForm(request.POST)
		user_form = RegisterUserForm(request.POST)
		org_form = OrganizationForm(request.POST)
		if meta_form.is_valid():
			org = org_form.save()

			user = user_form.save(commit=False)
			email = user_form.cleaned_data['email']
			user.username = email
			user.email = email
			content_type = ContentType.objects.get_for_model(Organization)
			manage_perm = Permission.objects.get(content_type=content_type, codename='access_watsan')
			user.save()
			user.user_permissions.add(manage_perm)

			meta = meta_form.save(commit=False)
			meta.user = user 
			meta.organization = org
			if(request.POST.get('question_1_other')):
				meta.question_1 = request.POST.get('question_1_other')

			if(request.POST.get('question_2_other')):
				meta.question_2 = request.POST.get('question_2_other')

			meta.save()

			loggedInUser = authenticate(username=user.username, password=user_form.clean_password())
			login(request, loggedInUser)
			return redirect('/dashboard/')
			
		return render(request, 'registration/register_final_questions.html', {'meta_form': meta_form, 'user_form': user_form, 'org_form': org_form })
	else:
		meta_form = UserMetaForm()
		return render(request, 'registration/register_final_questions.html', { 'meta_form': meta_form})
