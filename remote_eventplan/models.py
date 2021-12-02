from django.db import models

# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=100, default="")
    target = models.CharField(max_length=20, default="誰でも")
    person = models.CharField(max_length=20, default="")
    category = models.CharField(max_length=30, default="その他")
    time = models.CharField(max_length=100, default="")
    tools = models.CharField(max_length=100, default="")
    help = models.CharField(max_length=100, default="")
    outline = models.CharField(max_length=200, default="")
    posted_at = models.DateTimeField('date published')
    like = models.IntegerField(default=0)