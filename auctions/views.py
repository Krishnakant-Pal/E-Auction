from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count,Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.utils import timezone
from django.urls import reverse
from . import form
from .models import *

def index(request):
    listings = Listing.objects.all()
    
    return render(request, "auctions/index.html",{
        "listings":listings,
    })

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
def create_listing(request):

    if request.method == "POST":
        new_listing  = form.NewListingForm(request.POST)

        if new_listing.is_valid():
            owner = request.user.username
            title = new_listing.cleaned_data['title']
            description = new_listing.cleaned_data['description']
            ask_price = new_listing.cleaned_data['ask_price']
            category = new_listing.cleaned_data['category']
            imagelink = new_listing.cleaned_data['imagalink']
            listing = Listing.objects.create(owner=owner,title=title, 
                        description=description,ask_price=ask_price, category=category,
                        imagelink=imagelink)
            listing.save()
            messages.success(request,'Data has been submitted')
            return redirect(reverse('create_listing') )
    
    return render(request, "auctions/create_listing.html",{
         "form": form.NewListingForm()
         })


def listing_details(request,listing_title): 

    product = Listing.objects.get(title=listing_title)
    bids  = Bidding.objects.filter(listing=product.id)
    comments = Comment.objects.filter(listing=product.id)
    number_of_bids  = Bidding.objects.filter(listing=product.id).count()
    max_bid = bids.aggregate(max_bid = Max("bid_price"))["max_bid"]
        

    return render(request,"auctions/listing_details.html",{
        "product": product,
        "max_bid":max_bid,
        "number_of_bids": number_of_bids,
        "comments": comments,
         })
