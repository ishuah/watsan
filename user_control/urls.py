from django.conf.urls import *
    
urlpatterns = patterns('',
    url('', include('social.apps.django_app.urls', namespace='social')),
	(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'pages/login.html'}, 'default_login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/welcome/?next=/'}, 'default_logout'),

	(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'settings/password/change.html'}),
    (r'^password_change_done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'settings/password/change_done.html'}),
    (r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'settings/password/reset.html',
        'email_template_name': "email/reset_password.html",
        'post_reset_redirect': '/users/password_reset_done/'}, 'password_reset'),
    (r'^password_reset_done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'settings/password/reset_done.html'}, 'password_reset_done'),
    (r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/', 'template_name': 'settings/password/reset_confirm.html'}, 'password_reset_confirm'),
)

urlpatterns += patterns('user_control.views',
    (r'^delete/(?P<userIds>[\d,]{0,100})/$', 'delete_users'),
    url(r'^signup/$', 'signup', name='signup'),

    (r'^change_name/$', 'change_name'),
    (r'^change_email/$', 'change_email'),
    (r'^change_email_complete/(?P<hash_string>[0-9A-Za-z]+)/$', 'change_email_complete'),

    url(r'^confirm/(?P<confirmationCode>[\w\s\d]{0,20})/(?P<username>[\w\s\d]{0,50})/$', 'confirm', name="confirm"),
)