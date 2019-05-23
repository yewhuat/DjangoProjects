from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import date

class Restaurant(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zipCode = models.CharField(max_length=10, blank=True, null=True)
    stateOrProvince = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, default='Malaysia')
    telephone = models.CharField(max_length=20, blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, default=1)
    date = models.DateField(default=date.today)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return u"%s %s" % (self.name, self.stateOrProvince)

    def get_absolute_url(self):
        return reverse('app02:restaurant_detail', args=[str(self.id)])
        #return u"/app02/restaurants/%d" % self.id


class Dish(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField('RM', max_digits=8, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(User, default=1)
    date = models.DateField(default=date.today)
    #image = models.ImageField(upload_to="myrestaurants", blank=True, null=True)
    image = models.FileField(upload_to="myrestaurants", blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, null=True, related_name='dishes')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return u"%s %d" % (self.name, self.price)

    def get_absolute_url(self):
        return reverse('app02:restaurant_detail', args=[str(self.restaurant.id)])
        #return reverse('app02:dish_detail', args=[str(self.restaurant.id), str(self.id)])
        #return u"/app02/restaurants/%d/dishes/%d" % (self.restaurant.id, self.id)

class Review(models.Model):
    RATING_CHOICES = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
    rating = models.PositiveSmallIntegerField('Rating (stars)', blank=False, default=3, choices=RATING_CHOICES)
    comment = models.TextField(max_length = 1000, blank=True, null=True)
    user = models.ForeignKey(User, default=1)
    date = models.DateField(default=date.today)

    class Meta:
        abstract = True

class RestaurantReview(Review):
    restaurant = models.ForeignKey(Restaurant)

    def __str__(self):
        return u"%s %s %s" % (self.restaurant, self.user, self.date)


