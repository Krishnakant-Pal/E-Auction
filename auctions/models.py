from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

CATEGORIES_CHOICES = {
        ("Elec","Electronics"),
        ("Clo","Clothing"),
        ("B" ,"Books"),
        ("H&K","Home & Kitchen"),
        ("T", "Toys"),

}
class Listing(models.Model):
    owner = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=248)
    ask_price = models.IntegerField()
    category  = models.CharField(max_length=5,choices=CATEGORIES_CHOICES,null=True)
    creation_date = models.DateTimeField(auto_now=True)
    imagelink = models.CharField(max_length=128,default=False)
   
    def __str__(self):
        return f"Owner:{self.owner},Title: {self.title},Ask_Price: {self.ask_price},Category: {self.category},Creation_Date: {self.creation_date}"

class Bidding(models.Model):
    user = models.CharField(max_length=64)
    bid_price = models.IntegerField()
    number_of_item = models.IntegerField()
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)

    def __str__(self):
        return f"User:{self.user} ,Bid Price {self.bid_price},No. of items:{self.number_of_item},listing: {self.listing}"

class Comment(models.Model):
    user = models.CharField(max_length=64)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    comment = models.CharField(max_length=248)

    def __str__(self):
        return f"user:{self.user},listing: {self.listing},Comment: {self.comment}"

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)


