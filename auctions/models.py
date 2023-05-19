from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage as storage

# Validator for my image table
def validate_image_extension(value):
    ext = value.name.split('.')[-1]
    valid_extensions = ['jpg', 'jpeg', 'png']
    if ext not in valid_extensions:
        raise ValidationError(('Invalid image file type.'))

class User(AbstractUser):
    """"Users table is created by default by the class AbstractUser"""
    
    watchlist = models.ManyToManyField("Listing", related_name='watchers', blank=True)


class Listing(models.Model):
    """"The table that will hold the listing name, details text, starting bid(is also hoghest bid),
    date when it was posted,it's state closed or open, a category and finally an image"""
    
    name = models.CharField(max_length=120)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="listing")
    open = models.BooleanField(default=True)
    # current available categories of listings
    CATEGORY_CHOICES = (
        ('Electronics', 'Electronics'),
        ('Fashion', 'Fashion'),
        ('Home & Garden', 'Home & Garden'),
        ('Toys & Hobbies', 'Toys & Hobbies'),
        ('Collectibles & Art', 'Collectibles & Art'),
        ('Sporting Goods', 'Sporting Goods'),
        ('Health & Beauty', 'Health & Beauty'),
        ('Motors', 'Motors'),
        ('Business & Industrial', 'Business & Industrial'),
        ('Other', 'Other'),
    )
    category = models.CharField(max_length=50 ,choices=CATEGORY_CHOICES)
    # To make he listimng always sorted
    class Meta:
        ordering = ["-date"]
    
    
class ListingImage(models.Model):
    """The table table that will hold the images of a listing"""
    
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="theImages")
    images = models.ImageField(upload_to="media_night/auctions/Images/Listings/", storage=storage, validators=[validate_image_extension])
    
    
class Bid(models.Model):
    """"Bids table will contain all the bids that are placed on a certain listing by a certain user"""
    
    bid = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="bids")
    class Meta:
        ordering = ["-bid"]
    
    
class Comment(models.Model):
    """Table that will contain the comments of users on a listing"""
    
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="comments")
    date_added = models.DateTimeField(auto_now_add=True)