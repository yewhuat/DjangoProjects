from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from .models import RestaurantReview, Restaurant, Dish
from .forms import RestaurantForm, DishForm

# rest_framework
from rest_framework import viewsets, authentication, permissions
from .serializers import RestaurantSerializer

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'app02/signup.html'


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

