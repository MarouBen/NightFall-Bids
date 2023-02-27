from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Listing

def index(request):
    return render(request, "auctions/index.html")


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


def create(request):
    if request.method == "POST":
        
        Title = request.POST.get("T","")
        
        Bid = request.POST.get("B","")
            
        Description = request.POST.get("D","")
        Image = request.FILES.get("I","")
        
        if not Title:
            return render(request, "auctions/create.html",{"is_title" : "is-invalid","D":Description,"B":Bid})
        if not Bid:
            return render(request, "auctions/create.html",{"is_bid" : "is-invalid","T":Title,"D":Description})
        if not Image :
            return render(request, "auctions/create.html",{"is_image" : "is-invalid","T" :Title,"D":Description,"B":Bid})
            
        new_listing = Listing(name=Title, 
                    description=Description, 
                    startingBid=Bid, 
                    image=Image)
        new_listing.save()
        return render(request,"auctions/index.html")
            
    else:
        return render(request, "auctions/create.html")