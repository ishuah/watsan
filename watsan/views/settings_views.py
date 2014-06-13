import json
import uuid
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from watsan.models import WatsanUserMeta, Organization, NewEmail
from watsan.models.forms import AddUserForm, EditUserNameForm, ChangeUserEmailForm
from django.core.mail import send_mail
from django.http import HttpResponse

@login_required(login_url='/watsan/login/?next=/watsan')
def settings(request):
	meta = WatsanUserMeta.objects.get(user=request.user)
	members = WatsanUserMeta.objects.filter(organization=meta.organization)
	adduserform = AddUserForm()

	if request.method == 'POST':
		adduserform = AddUserForm(request.POST)
		if adduserform.is_valid():
			if adduserform.clean_email2():
				user = adduserform.save(commit=False)
				user.username = user.email

				password = User.objects.make_random_password()
				user.set_password(password)
				user.save()
				meta = WatsanUserMeta.objects.get(user=request.user)
				new_meta = WatsanUserMeta(user=user, organization=meta.organization)
				new_meta.save()
				#email added user
				#TODO: change register_url 
				message = render_to_string('watsan/email/welcome.html', {'password': password, 'invite_from': request.user, 'register_url':'http://localhost:8000/watsan/login'})
				send_mail('Welcome!', message, 'kariuki@ishuah.com', [user.email])
				adduserform = AddUserForm()

				return render(request, 'watsan/dashboard/settings.html', { 'meta': meta, 'members': members, 'adduserform': adduserform, 'message': user.email+" added!" })

			return render(request, 'watsan/dashboard/settings.html', { 'meta': meta, 'members': members, 'adduserform': adduserform })
		else:
			return render(request, 'watsan/dashboard/settings.html', { 'meta': meta, 'members': members, 'adduserform': adduserform })
	else:
		return render(request, 'watsan/dashboard/settings.html', { 'meta': meta, 'members': members, 'adduserform': adduserform })


@login_required(login_url='/watsan/login/?next=/watsan')
def change_user_name(request):

	if request.method == 'POST':
		new_name = EditUserNameForm(request.POST).save(commit=False)
		request.user.first_name = new_name.first_name
		request.user.last_name = new_name.last_name
		request.user.save();
		return redirect('/watsan/settings')
	else:
		new_name_form = EditUserNameForm({'first_name': request.user.first_name, 'last_name': request.user.last_name })
		return render(request, 'watsan/dashboard/change_user_name.html', { 'new_name_form': new_name_form })

@login_required(login_url='/watsan/login/?next=/watsan')
def change_user_email(request):
	if request.method == 'POST':
		new_email_form = ChangeUserEmailForm(request.POST)
		if new_email_form.is_valid():
			new_email = new_email_form.save(commit=False)

			if User.objects.filter(email=new_email.email).exists():
				new_email_form._errors['email'] = new_email_form.error_class([u"That email is already registered."])
				return render(request, 'watsan/dashboard/change_user_email.html', {'new_email_form': new_email_form })
			else:
				new_email.user = request.user
				new_email.hash_string = uuid.uuid1().hex[:9]
				transfered = False
				new_email.save()

				message = render_to_string('watsan/email/change_email.html', { 'link': 'http://localhost:8000/watsan/settings/change_user_email_complete/'+new_email.hash_string })
				send_mail('Changing your watsan email', message, 'kariuki@ishuah.com', [new_email.email])

			return render(request, 'watsan/dashboard/change_user_email_done.html')
		else:
			return render(request, 'watsan/dashboard/change_user_email.html', {'new_email_form': new_email_form })
	else:
		new_email_form = ChangeUserEmailForm()
		return render(request, 'watsan/dashboard/change_user_email.html', {'new_email_form': new_email_form })

def change_user_email_complete(request, hash_string):
	try:
		new_email = NewEmail.objects.get(hash_string=hash_string)
	except:
		return render(request, 'watsan/dashboard/change_user_email_error.html')
	user = new_email.user 
	user.email = new_email.email
	user.username = new_email.email
	user.save()

	new_email.transfered = True
	new_email.hash_string = ''
	new_email.save()

	if request.user.is_authenticated():
		logout(request)

	return render(request, 'watsan/dashboard/change_user_email_complete.html')