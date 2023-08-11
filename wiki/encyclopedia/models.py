from django.db import models

# Create your models here.
class Catagory(models.Model):
    name = models.CharField(blank=True, max_length=64)


class Topic(models.Model):
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE, null=True)
    name = models.CharField(blank=True, max_length=64, null=True)