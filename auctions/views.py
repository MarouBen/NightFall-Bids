from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from .models import User,Listing,ListingImage,Bid,Comment


def index(request):
    # Here we get all the listing and the first image of each
    listings = Listing.objects.filter(open=True).all()
    context = {
        "listings" : listings
    }
    return render(request, "auctions/index.html",context)


def listings(request):
    listings = Listing.objects.all()      
    context = {
        "listings" : listings,
        "title" : "Active Listings",
        "Listing":Listing
    }
    return render(request,"auctions/search.html",context)


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
            return render(request, "auctions/login.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/login.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/login.html")


@login_required
def create(request):
    if request.method == "POST":
        
        Title = request.POST.get("T","").strip()
        bid = request.POST.get("B","").strip()
        Description = request.POST.get("D","").strip()
        Category = request.POST.get("C")
        Images = request.FILES.getlist("I")
        Owner = request.user

        # Saving the listing into it's table   
        new_listing = Listing(name=Title, 
                    description=Description, 
                    user=Owner,
                    category=Category)
        new_listing.save()
        
        new_bid = Bid(
            bid=bid,
            user=request.user,
            listing=new_listing
        )
        new_bid.save()
        
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
    
@never_cache
def item_view(request, pk, message=None):
    # Get the item and it's images
    Item = Listing.objects.get(pk=pk)
    state = Item.open
    Images = [img.images.url for img in Item.theImages.all()]
    
    # Is it in the watchlist of the user
    ## Per default it's in false
    ### also getting info if the user is the owner
    watched = False
    owner = False
    if request.user.is_authenticated:
        user = request.user
        if Item in user.watchlist.all():
            watched = True
        if Item.user == user:
            owner = True
            
    # Getting the comments of the Item
    comments = Item.comments.order_by("-date_added")
    context = {
        "listing":Item,
        "images":Images,
        "watched":watched,
        "open" : state,
        "message":message,
        "owner":owner,
        "comments":comments 
    }
    return render(request, "auctions/item.html",context)


@login_required
def watchlist(request):
    user = request.user
    if request.method == 'POST':
        listing_pk = request.POST.get('watch')
        listing = Listing.objects.get(pk=listing_pk)
        
        if request.POST.get("action") == "add":
            user.watchlist.add(listing)
        else:
            user.watchlist.remove(listing)
    
        return redirect("watchlist")
    
    # If the user is not loged in
    if not request.user.is_authenticated:
        return redirect("login")
    
    watched_listings = user.watchlist.all()     
    context = {
        "listings" : watched_listings,
        "title" : "Watchlist",
        "user" : user
    }
    return render(request,"auctions/watchlist.html",context)


@login_required
def bid(request):
    # If the user is not loged in
    if not request.user.is_authenticated:
        return redirect("login")
    listing_pk = request.POST.get("pk")
    user_bid = int(request.POST.get("B",0))
    listing = Listing.objects.get(pk=listing_pk)
    highestBid = int(listing.bids.first().bid)
    if user_bid > highestBid:
        new_bid = Bid(
            bid=user_bid,
            user=request.user,
            listing=listing
        )
        new_bid.save()
        return item_view(request,listing_pk,1)
    else:
        return item_view(request,listing_pk,0)
    
    
@login_required
def close(request):
    if request.method == "POST":
        pk = request.POST.get("pk")
        listing = Listing.objects.get(pk=pk)
        listing.open = False
        listing.save()
        print(listing.open)
        return redirect("view",pk=pk)
    
    
@login_required
def add_comment(request):
    if request.method == "POST":
        pk = request.POST.get("pk")
        listing = Listing.objects.get(pk=pk)
        comment = request.POST.get("comment")
        new_comment = Comment(
            comment=comment,
            user=request.user,
            listing=listing
        )
        new_comment.save()
        return redirect("view",pk=pk)
 
 
def view_search(request,context = None):
     if context == None:
         return render(request,"auctions/404.html")
     else :
         return render(request,"auctions/search.html",context)
 
    
def search(request):
    if request.method == "GET":
        query = request.GET.get("S")
        category = request.GET.get("category")
        state = request.GET.get("state")
        if state == "True":
            state = True
        elif state =="False":
            state = False
        try:
            if category:
                listing = Listing.objects.filter(name=query,category=category).first()
            else:
                listing = Listing.objects.filter(name=query).first()
            if listing is not None:
                pk = listing.pk
                return redirect("view",pk=pk)
        except Listing.DoesNotExist:
            pass
        
        searched_listings = []
        listings = Listing.objects.all()
        
        for listing in listings:
            if category:
                if query.upper().strip() in listing.name.upper() and category in listing.category:
                    searched_listings.append(listing)
            elif state != None: 
                if query.upper().strip() in listing.name.upper() and listing.open == state:
                    searched_listings.append(listing)
            else:
                if query.upper().strip() in listing.name.upper():
                    searched_listings.append(listing)
                    
        
        if searched_listings.__len__() > 0:
            if category:
                context = {
                    "listings":searched_listings,
                    "Listing":Listing,
                    "category":category
                }
            elif state != None:
                context = {
                    "listings":searched_listings,
                    "Listing":Listing,
                    "open":state
                }
            else:
                context = {
                    "listings":searched_listings,
                    "Listing":Listing,
                }
            return view_search(request,context)
        else:
            return view_search(request)
        
  
def categories(request, category):
    listings = Listing.objects.filter(category=category).all()
    context = {
                "listings":listings,
                "Listing":Listing,
                "category":category
            }
    return view_search(request,context)


def state(request, state):
    listings = Listing.objects.filter(open=state).all()
    if state == "True":
        state = True
    if state == "False":
        state = False
    context = {
                "listings":listings,
                "Listing":Listing,
                "open":state
            }
    return view_search(request,context)