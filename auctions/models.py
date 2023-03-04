from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Validator for my image table
def validate_image_extension(value):
    ext = value.name.split('.')[-1]
    valid_extensions = ['jpg', 'jpeg', 'png']
    if ext not in valid_extensions:
        raise ValidationError(('Invalid image file type.'))

class User(AbstractUser):
    """"Users table is created by default by the class AbstractUser"""
    pass


class Listing(models.Model):
    """"The table that will hold the listing name, details text, starting bid(is also hoghest bid),
    date when it was posted and finally an image"""
    
    name = models.CharField(max_length=64)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    startingBid = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])

    # current available categories of listings
    CATEGORY_CHOICES = (
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Books', 'Books'),
        ('Home & Garden', 'Home & Garden'),
        ('Sports & Outdoors', 'Sports & Outdoors'),
    )
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES)
    # To make he listimng always sorted
    class Meta:
        ordering = ["-date"]
    
    
class ListingImage(models.Model):
    """The table table that will hold the images of a listing"""
    
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="theImages")
    images = models.ImageField(upload_to="auctions/Images/Listings/", validators=[validate_image_extension])
    
    
class Bid(models.Model):
    """"Bids table will contain all the bids that are placed on a certain listing by a certain user"""
    
    bid = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def bidMinValue(self):
        if self.bid < self.listing.startingBid:
            raise ValidationError("Bid must be higher than the highest bid!")
    
    
class Comment(models.Model):
    """Table that will contain the comments of users on a listing"""
    
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)