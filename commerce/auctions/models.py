from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import User
from django.db import models






class AuctionsListing(models.Model):
    catagory = [
        ('Electronics', 'Electronics'),
        ('Fashion', 'Fashion'),
        ('Art', 'Art'),
        ('Archaeological', 'Archaeological')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    discription = models.TextField()
    starting_bid = models.DecimalField(max_digits=14, decimal_places=2, blank=True)
    imageurl = models.URLField()
    active = models.BooleanField(default=True)
    catagory = models.CharField(max_length=100, blank=True, choices=catagory)
    createddate = models.DateTimeField(auto_now_add=True)
    winner = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.id} : {self.title}  {self.user.username}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ListingID = models.IntegerField(blank=True)
    
    def __str__(self) :
        return f"{self.user} {self.ListingID}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listingid = models.IntegerField(blank=True)
    bid = models.IntegerField(blank=True)
    def __str__(self) :
        return f"{self.id}: {self.user}:{self.bid}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    listingid = models.IntegerField(blank=True)
    def __str__(self):
        return f"{self.listingid} : {self.user} --->> comment : {self.comment} {self.time}"

class Close(models.Model):
    winner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.CharField(max_length=64, blank=True)
    listingid = models.IntegerField(blank=True)
    winprice = models.IntegerField()
    def __str__(self):
        return f"{self.owner} sold to {self.winner}"