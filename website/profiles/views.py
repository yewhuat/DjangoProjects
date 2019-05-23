from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactUsForm, UserForm, UserProfileForm, ContactUsFormCrispy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import View
from allauth.account.views import PasswordChangeView

from django.contrib.auth import get_user_model
#User = get_user_model()

"""
    url(r'^$', profiles_views.home, name='home'),
def home(request):
    context = locals()
    template = 'home.html'
    return render(request, template , context)
"""

class HomeView(View):

    def get(self, request, *args, **kwargs):
        context = locals()
        template = 'home.html'
        return render(request, template, context)

class ContactUsView(View):

    def get(self, request, *args, **kwargs):
        title = 'Contact US'
        form = ContactUsForm(request.POST or None)
        #form = ContactUsFormCrispy(request.POST or None)
        confirm_message= None

        if form.is_valid():
            #print(request.POST)
            #print(form.cleaned_data)
            subject = 'MESSAGE FROM DJANGO: %s %s %s %s %s' %(form.cleaned_data['category'], form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['mobileno'], form.cleaned_data['subject'])
            message = form.cleaned_data['message']
            emailfrom = form.cleaned_data['email']
            emailto = [settings.EMAIL_HOST_USER]
            send_mail(subject,message,emailfrom,emailto,fail_silently=True)
            title = "Thanks"
            confirm_message = "Thanks for the message. We will get back to you"
            form.save()
            form = None

        context = {'title' : title, 'form': form, 'confirm_message': confirm_message, }
        template = 'contactus.html'
        return render(request, template , context)

"""
def about(request):
    context = locals()
    template = 'about.html'
    return render(request, template , context)
"""

class UserProfileView(LoginRequiredMixin, View):
    form = ''
    context = ''
    template = 'userprofile.html'

    def get(self, request, *args, **kwargs):
        userForm = UserForm(instance=request.user)
        userProfileForm = UserProfileForm(instance=request.user.profile)
        context = {'userForm': userForm, 'userProfileForm': userProfileForm}
        return render(request, self.template, context)

    #@transaction.atomic
    def post(self, request, *args, **kwargs):
        userForm = UserForm(request.POST, instance=request.user)
        userProfileForm = UserProfileForm(request.POST, instance=request.user.profile)
        if userForm.is_valid() and userProfileForm.is_valid():
            userForm.save()
            userProfileForm.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('userprofile')
        else:
            messages.error(request, 'Please correct the error below')

        context = {'userForm': userForm, 'userProfileForm': userProfileForm}
        return render(request, self.template , context)

class CustomPasswordChangeView(PasswordChangeView):

    @property
    def success_url(self):
        pass
