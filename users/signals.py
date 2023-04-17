# Signals are use to dispatch multiple other requests, for eg when user is created or profile is created an email can be triggered 
# to the user
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete

# This is a decorator
from django.dispatch import receiver
# To get the default User from DB and all of the details of the user
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile



# Using this is a decorator is also an option instead of specifying it seperatly and connecting the function with post_save method.
# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name, # Profile name
        )

        subject = 'Welcome to my app'
        message = 'I wish you have a nice chat with the other developers'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,

        )

def updateUser(sender, instance, created, **kwargs):
    
    profile = instance
    # Since profile and user are one to one relationship we can get data both ways, i.e from profile we get user as below and vice verse
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    user=instance.user
    user.delete()

post_save.connect(createProfile, sender=User)

post_save.connect(updateUser, sender=Profile)

post_delete.connect(deleteUser, sender=Profile)