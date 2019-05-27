from django.core.urlresolvers import reverse, reverse_lazy
#Use Customer User Model, therefore disable django UserCreationForm
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from django.contrib.sites.shortcuts import get_current_site
#from django.utils.encoding import force_bytes
#from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage

from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_activation_token
from .models import RestaurantReview, Restaurant, Dish
from .forms import UserAdminCreationForm, RestaurantForm, DishForm

# rest_framework
from rest_framework import viewsets, authentication, permissions
from .serializers import RestaurantSerializer

User = get_user_model()

class SignUp(CreateView):
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('login')
    template_name = 'app02/signup.html'

    def post(self, request):
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            # Create an inactive user with no password:
            user = form.save(commit=False)
            user.is_active = False
            #user.set_unusable_password()
            user.save()

            # Send an email to the user with the token:
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
            message = "Hello {0},\n {1}".format(user.username, activation_link)
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            #login(request, user)
            #form = PasswordChangeForm(request.user)
            #return render(request, 'activation.html', {'form': form})
            return HttpResponse('Account successfully activated')

        else:
            return HttpResponse('Activation link is invalid!')

    # def post(self, request):
    #     form = PasswordChangeForm(request.user, request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         update_session_auth_hash(request, user) # Important, to update the session with the new password
    #         return HttpResponse('Password changed successfully')


class RestaurantDetail(LoginRequiredMixin, DetailView):
    model = Restaurant
    template_name = 'app02/restaurant_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RestaurantDetail, self).get_context_data(**kwargs)
        context['RATING_CHOICES'] = RestaurantReview.RATING_CHOICES
        return context


class RestaurantCreate(LoginRequiredMixin, CreateView):
    model = Restaurant
    template_name = 'app02/form.html'
    form_class = RestaurantForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(RestaurantCreate, self).form_valid(form)


class DishCreate(LoginRequiredMixin, CreateView):
    model = Dish
    template_name = 'app02/form.html'
    form_class = DishForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
        return super(DishCreate, self).form_valid(form)


def review(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    review = RestaurantReview(
        rating=request.POST['rating'],
        comment=request.POST['comment'],
        user=request.user,
        restaurant=restaurant)
    review.save()
    return HttpResponseRedirect(reverse('app02:restaurant_detail', args=(restaurant.id,)))


class DefaultMixin(object):
    """Default settings for view authentication, permissions, filtering and pagination"""

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

class RestaurantViewSet(DefaultMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating restaurants"""
    queryset = Restaurant.objects.order_by('name')
    serializer_class = RestaurantSerializer

