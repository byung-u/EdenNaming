# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from .choices import (GENDER_CHOICES, ORDER_CHOICES,
                      LASTNAME_CHOICES, LOCATION_CHOICES)


class NamingUserInput(models.Model):
    gender = models.IntegerField(choices=GENDER_CHOICES, default=2)
    birth_order = models.IntegerField(choices=ORDER_CHOICES, default=1)
    location = models.IntegerField(choices=LOCATION_CHOICES, default=7)
    last_name = models.IntegerField(choices=LASTNAME_CHOICES, default=2)
    birth_datetime = models.DateTimeField(default=timezone.now)
    #birth_datetime = models.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])

    def __str__(self):
        return self.name
