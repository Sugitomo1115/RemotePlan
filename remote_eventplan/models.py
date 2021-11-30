from django.db import models

# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=100)
    target = models.CharField(max_length=20)
    person = models.CharField(max_length=20)
    time = models.CharField(max_length=100)
    tools = models.CharField(max_length=100)
    help = models.CharField(max_length=100)
    outline = models.CharField(max_length=200)
    posted_at = models.DateTimeField('date published')
    like = models.IntegerField(default=0)