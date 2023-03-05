from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import User,Listing,ListingImage


def view_listings(request,context):
    return render(request,"auctions/listings.html",context)


def index(request):
    # Here we get all the listing and the first image of each
    listings = Listing.objects.all()
    context = {
        "listings" : listings
    }
    return render(request, "auctions/index.html",context)


def listings(request):
    listings = Listing.objects.all()      
    context = {
        "listings" : listings,
        "title" : "Active Listings"
    }
    return view_listings(request,context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        
        Title = request.POST.get("T","").strip()
        Bid = request.POST.get("B","").strip()
        Description = request.POST.get("D","").strip()
        Category = request.POST.get("C")
        Images = request.FILES.getlist("I")
        Owner = request.user
        print(Category)
        # Saving the listing into it's table   
        new_listing = Listing(name=Title, 
                    description=Description, 
                    startingBid=Bid, 
                    user=Owner,
                    category=Category)
        new_listing.save()
        
        # Save the images into the images table related the the listing
        for Image in Images:
            new_listing_image = ListingImage(listing=new_listing ,images=Image)
            new_listing_image.save()
        
        return redirect("index")
    
    # If the user is not loged in
    if not request.user.is_authenticated:
        return redirect("login")
   
    return render(request, "auctions/create.html",{
        "categories" : Listing.CATEGORY_CHOICES
    })
    
    
def item_view(request, pk):
    # Get the item and it's images
    Item = Listing.objects.get(pk=pk)
    Images = [img.images.url for img in Item.theImages.all()]
    context = {
        "listing":Item,
        "images":Images
    }
    return render(request, "auctions/item.html",context)


@login_required
def watchlist(request):
    user = request.user
    if request.method == 'POST':
        listing_pk = request.POST.get('watch')
        listing = Listing.objects.get(pk=listing_pk)
        
        user.watchlist.add(listing)
        return redirect("watchlist")
    
    # If the user is not loged in
    if not request.user.is_authenticated:
        return redirect("login")
    
    watched_listings = user.watchlist.all()     
    context = {
        "listings" : watched_listings,
        "title" : "Watchlist"
    }
    return view_listings(request,context)