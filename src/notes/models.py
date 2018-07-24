# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

from django.db import models

# Create your models here.

class Entry(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL)
	title=models.CharField(max_length=120)
	description=models.TextField()
	timestamp=models.DateTimeField(auto_now_add=True)
	updated= models.DateTimeField(auto_now=True)
	image=models.ImageField(null=True, blank=True)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return "/entries/{0}/".format(self.id)

	def get_update_url(self):
		return "/entries/{0}/update".format(self.id)

	def get_delete_url(self):
		return "/entries/{0}/delete".format(self.id)
