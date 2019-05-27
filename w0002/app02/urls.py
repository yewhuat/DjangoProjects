from django.conf.urls import url
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView
from .models import Restaurant, Dish
from .forms import RestaurantForm, DishForm
from .views import SignUp, Activate, RestaurantCreate, RestaurantDetail, DishCreate, review, RestaurantViewSet
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'rest_restaurants', RestaurantViewSet.as_view())
router.register(r'rest_restaurants', views.RestaurantViewSet)

urlpatterns = [

    url(r'^signup/$', SignUp.as_view(), name='signup'),

    url(r'^activate/<str:uid>/<str:token>', Activate.as_view(), name='activate'),

    # List latest 5 restaurants: /app02/
    url(r'^$',
        ListView.as_view(
            queryset=Restaurant.objects.filter(date__lte=timezone.now()).order_by('date')[:50],
            context_object_name='latest_restaurant_list',
            template_name='app02/restaurant_list.html'),
        name='restaurant_list'),

    url(r'^restaurant/create/$',
        RestaurantCreate.as_view(),
        name='restaurant_create'),

    url(r'^restaurants/(?P<pk>\d+)/$',
        RestaurantDetail.as_view(),
        name='restaurant_detail'),

    # Edit restaurant details, ex.: /restaurants/1/edit/
    url(r'^restaurants/(?P<pk>\d+)/edit/$',
        UpdateView.as_view(
            model=Restaurant,
            template_name='app02/form.html',
            form_class=RestaurantForm),
        name='restaurant_edit'),

    # Restaurant dish details, ex: /restaurants/1/dishes/1/
    url(r'^restaurants/(?P<pkr>\d+)/dishes/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Dish,
            template_name='app02/dish_detail.html'),
        name='dish_detail'),

    # Create a restaurant dish, ex.: /restaurants/1/dishes/create/
    url(r'^restaurants/(?P<pk>\d+)/dishes/create/$',
        DishCreate.as_view(),
        name='dish_create'),

    # Edit restaurant dish details, ex.: /restaurants/1/dishes/1/edit/
    url(r'^restaurants/(?P<pkr>\d+)/dishes/(?P<pk>\d+)/edit/$',
        UpdateView.as_view(
            model=Dish,
            template_name='app02/form.html',
            form_class=DishForm),
        name='dish_edit'),

    # Create a restaurant review, ex.: /myrestaurants/restaurants/1/reviews/create/
    # Unlike the previous patterns, this one is implemented using a method view instead of a class view
    url(r'^restaurants/(?P<pk>\d+)/reviews/create/$',
        review,
        name='review_create'),
]
