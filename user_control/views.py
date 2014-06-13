from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.models import Site
from user_control.models import NewUserForm, UserProfile
from user_control import utils

def signup(request):
    if request.method == "POST":
        user_form = NewUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            confirmation_code = utils.generate_confirmation_code()
            userprofile = UserProfile(user=user, confirmation_code=confirmation_code)
            userprofile.save()
            
            html_content = render_to_string('email/confirmation.html', { 'username': user.username, 'confirmation_code': confirmation_code, 'domain': Site.objects.get_current().domain })
            text_content = strip_tags(html_content) 
            message = EmailMultiAlternatives('Email Confirmation', text_content, 'connect@spatialcollective.com', [user.email])
            message.attach_alternative(html_content, "text/html")
            message.send()

            return render(request, 'pages/signup.html')
        return render(request, 'pages/signup.html', {'userform': user_form})
    else:
        user_form = NewUserForm()
        return render(request, 'pages/signup.html', {'userform': user_form})


def confirm(request, confirmationCode, username):
	user = User.objects.get(username=username)
	profile = UserProfile.objects.get(user=user)

	if profile.confirmation_code == confirmationCode:
		profile.confirmation_code = ''
		profile.save()
		user.save()

		html_content = render_to_string('email/welcome.html', { 'username': user.username })
		text_content = strip_tags(html_content) 
		message = EmailMultiAlternatives('Welcome to Spatial Collective!', text_content, 'connect@spatialcollective.com', [user.email])
		message.attach_alternative(html_content, "text/html")
		message.send()
		
		user.backend='django.contrib.auth.backends.ModelBackend'
		login(request, user)
	return redirect('home')



@login_required
def change_name(request):
	if request.method == 'POST':
		new_name = EditUserNameForm(request.POST).save(commit=False)
		request.user.first_name = new_name.first_name
		request.user.last_name = new_name.last_name
		request.user.save();
		return redirect('/settings')
	else:
		new_name_form = EditUserNameForm({'first_name': request.user.first_name, 'last_name': request.user.last_name })
		return render(request, 'settings/change_name.html', { 'new_name_form': new_name_form })

@login_required
def change_email(request):
	if request.method == 'POST':
		new_email_form = ChangeUserEmailForm(request.POST)
		if new_email_form.is_valid():
			new_email = new_email_form.save(commit=False)

			if User.objects.filter(email=new_email.email).exists():
				new_email_form._errors['email'] = new_email_form.error_class([u"That email is already registered."])
				return render(request, 'settings/email/change.html', {'new_email_form': new_email_form })
			else:
				new_email.user = request.user
				new_email.hash_string = uuid.uuid1().hex[:9]
				transfered = False
				new_email.save()

				message = render_to_string('watsan/email/change.html', { 'link': 'http://localhost:8000/watsan/settings/change_user_email_complete/'+new_email.hash_string })
				send_mail('Changing your email', message, 'kariuki@ishuah.com', [new_email.email])

			return render(request, 'settings/email/change_done.html')
		else:
			return render(request, 'settings/email/change.html', {'new_email_form': new_email_form })
	else:
		new_email_form = ChangeUserEmailForm()
		return render(request, 'settings/email/change.html', {'new_email_form': new_email_form })

def change_email_complete(request, hash_string):
	try:
		new_email = NewEmail.objects.get(hash_string=hash_string)
	except:
		return render(request, 'settings/email/change_error.html')
	user = new_email.user 
	user.email = new_email.email
	user.username = new_email.email
	user.save()

	new_email.transfered = True
	new_email.hash_string = ''
	new_email.save()

	if request.user.is_authenticated():
		logout(request)

	return render(request, 'settings/email/change_complete.html')

@permission_required('base_map.manage_map')
def delete_users(request, userIds=None):
	user_id_list = filter (lambda i:  i != ' ', userIds.split(','))
	count = 0
	for u  in user_id_list:
		if u and not User.objects.get(pk=u) == request.user:
			User.objects.get(pk=u).delete()
			count += 1
		elif u:
			messages.error(request, "Sorry, you can't delete yourself yet!")
	if count > 0:
		messages.success(request, "Deleted %i users" % (count))
	return redirect('/settings/members/')