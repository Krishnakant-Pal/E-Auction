from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count,Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.urls import reverse
from . import form
from .models import *

def index(request):
    """ Get all the Active listings and return them"""

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
    """ Lets user create a listing """
    if request.method == "POST":
        new_listing  = form.NewListingForm(request.POST)

        if new_listing.is_valid():
            owner = request.user
            title = new_listing.cleaned_data['title']
            description = new_listing.cleaned_data['description']
            ask_price = new_listing.cleaned_data['ask_price']
            category = new_listing.cleaned_data['category']
            imagelink = new_listing.cleaned_data['imagalink']
            listing = Listing.objects.create(owner=owner,title=title, 
                        description=description,ask_price=ask_price, category=category,
                        imagelink=imagelink)
            
            messages.success(request,'Data has been submitted')
            return redirect(reverse('create_listing') )
    
    return render(request, "auctions/create_listing.html",{
         "form": form.NewListingForm()
         })

def get_listing_details(listing_title):
    product = get_object_or_404(Listing, title=listing_title)
    bids  = Bidding.objects.filter(listing=product.id)
    max_bid = bids.aggregate(max_bid = Max("bid_price"))["max_bid"]
    comments = Comment.objects.filter(listing=product.id)
    number_of_bids  = Bidding.objects.filter(listing=product.id).count()
    
    # Incase of no bidding maxbid is equal to ask price
    if not max_bid:
        max_bid = product.ask_price

    return product, max_bid, comments, number_of_bids


def listing_details(request,listing_title): 

    product, max_bid, comments, number_of_bids = get_listing_details(listing_title)
    in_watchlist = Watchlist.objects.filter( listing=product,user = request.user)
   
    if request.method == "POST":
        # If user is not logged in then redirect to login page
        if not request.user.is_authenticated:
            return render(request, "auctions/login.html")

        bid_form = form.BidForm(request.POST)

        
        if bid_form.is_valid():
            new_bid_price = bid_form.cleaned_data['bid_price']            
            if new_bid_price <= max_bid :
                # bid is less than maxbid then return with message
                message = "Bid price should be more that current price"
            else: 
                # Accepts the new bid
                new_bid = Bidding.objects.create(user=request.user,bid_price=new_bid_price, 
                            number_of_item=1,listing=product)
                return redirect('listing_details', listing_title=listing_title)
            
    else:
            bid_form = form.BidForm()

    return render(request,"auctions/listing_details.html",{
        "product": product,
        "max_bid":max_bid,
        "number_of_bids": number_of_bids,
        "comments": comments,
        "in_watchlist": in_watchlist,
        "bid_form": form.BidForm,
        "message": message if request.method == "POST" else None
         })


@login_required
def add_to_watchlist(request,listing_title):
    listing = get_object_or_404(Listing, title=listing_title)
    already_exits = Watchlist.objects.filter( listing=listing,user = request.user)
    # Check if listing is already present in watchlist
    if already_exits:
        # remove listing from watchlist
        already_exits.delete()
       
    else:
        # add listing to watchlist
        new_watchlist = Watchlist.objects.create(user=request.user, listing=listing)

    return redirect(reverse('listing_details',args=[listing_title]) )