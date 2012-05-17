# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Profile(models.Model):
    
    user = models.OneToOneField(User, primary_key=True)
    suscripcion = models.DateField(default=datetime.now)
    doctor = models.BooleanField(default=True)

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
