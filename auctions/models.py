from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """"Users table is created by default by the class AbstractUser"""
    pass

class Listing(models.Model):
    """"The table that will hold the listing name, details text, starting bid,
    date when it was posted and finally an image"""
    
    # The id is created automatically
    name = models.CharField(max_length=64)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    startingBid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="Images/Listings/")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
class Bid(models.Model):
    """"Bids table will contain all the bids that are placed on a certain listing by a certain user"""
    
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
class Comment(models.Model):
    """Table that will contain the comments of users on a listing"""
    
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)