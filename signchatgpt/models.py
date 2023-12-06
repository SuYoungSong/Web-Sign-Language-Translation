from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class ImageCount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    count = models.IntegerField(default=0)


class ImageRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=False)
    question = models.CharField(max_length=300, null=False, blank=False)
    answer = models.CharField(max_length=500, null=False)
    pub_datetime = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateField(auto_now=True)
    page = models.IntegerField(null=False)