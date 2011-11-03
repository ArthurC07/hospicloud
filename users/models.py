# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    
    user = models.ForeignKey(User, unique=True)

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
