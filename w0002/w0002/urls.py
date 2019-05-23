"""w0002 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from app02.urls import router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^app02/', include('app02.urls', namespace='app02')),
    url(r'^$', RedirectView.as_view(url='/app02/', permanent=True)),
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    url(r'^api/', include(router.urls)),
]

#LogoutView, PasswordResetView, PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
#url(r'^accounts/logout/$', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
#url(r'^accounts/password_change/$', PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
#url(r'^accounts/password_change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
#url(r'^password_reset/$', PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
#url(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
#url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
#url(r'^reset/done/$', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
