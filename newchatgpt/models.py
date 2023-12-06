from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class ChatUserCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    count = models.IntegerField(default=0)


class ChatRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    question = models.CharField(max_length=300, null=False, blank=True)
    answer = models.TextField(max_length=500, null=False)
    pub_datetime = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateField(auto_now_add=True)
    page = models.IntegerField(null=False)
