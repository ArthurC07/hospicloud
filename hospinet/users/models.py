# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
    
    user = models.OneToOneField(User, primary_key=True)
    suscripcion = models.DateField(default=datetime.now)
    doctor = models.BooleanField(default=False)
    suscriptor = models.ForeignKey(User, blank=True, null=True,
                                   related_name='dependientes')

    def __unicode__(self):
        return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Hospital(models.Model):

    nombre = models.CharField(max_length=200)
