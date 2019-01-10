'''
Use Django signals to automatically create a profile when a new user is saved to
to the database:
    post_save is the signal that is sent after an object is saved
    User model is the model that sends the signal - the sender
    receiver is the method that allows receiver model to get the signal - a function that gets the signal and
        performs some task
    Profile is the receiver model that gets created by the reciever
'''
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
