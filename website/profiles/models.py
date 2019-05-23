from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nric = models.CharField(max_length=14)
    birth_date = models.DateField(null=False, default= '1900-01-01')
    address01 = models.CharField(max_length=255)
    address02 = models.CharField(max_length=255)
    address03 = models.CharField(max_length=255)
    state = models.CharField(max_length=20, default='Kuala Lumpur')
    postcode = models.CharField(max_length=10, default='50000')
    country = models.CharField(max_length=255, default='Malaysia')

    def __str__(self):    # __unicode__(self): on python 2
        return self.user

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


@receiver(post_save, sender=User)
def create_User_Profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_User_Profile(sender, instance, **kwargs):
    instance.profile.save()

class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobileno = models.CharField(max_length=15)
    category = models.IntegerField(default=0)
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=255)

    def __str__(self):    # __unicode__(self): on python 2
        return self.email

