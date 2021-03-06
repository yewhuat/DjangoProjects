from django.db import models
from django.conf import settings
#from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
## A new class is imported. ##
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from datetime import date


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        email = EmailMessage(subject, message, from_email, [self.email])
        email.send()


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
    #user = models.ForeignKey(User, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    #user = models.ForeignKey(get_user_model(), default=1)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    date = models.DateField(default=date.today)

    class Meta:
        abstract = True


class RestaurantReview(Review):
    restaurant = models.ForeignKey(Restaurant)

    def __str__(self):
        return u"%s %s %s" % (self.restaurant, self.user, self.date)

