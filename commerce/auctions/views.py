from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django import forms
from django.contrib import messages
from .models import AuctionsListing, WatchList, Bid, Comment, Close
from django.contrib.auth.decorators import login_required
from .forms import ListingForm, BidForm, CommentForm
from django.contrib.auth.models import User

def index(request):
    return render(request, "auctions/index.html", {
        "objects" : AuctionsListing.objects.all().order_by('-createddate')
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
# =======================================================


@login_required(login_url='auctions/login.html')
def CreateListing(request):
    
    return render(request, "auctions/create.html", context = {
        "form": ListingForm(),
    })
@login_required(login_url="auctions/login.html")
def insert(request):
    if request.method == "POST":
        form = ListingForm(request.POST,  request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            #Title = form.cleaned_data["title"]
            #Price = form.cleaned_data["price"]
            #Image = form.cleaned_data["imageurl"]
            #Catagory = form.cleaned_data["catagory"]
            #Discription = form.cleaned_data["discription"]
            #Starting_bid = form.cleaned_data["starting_bid"]
            #AuctionList = AuctionsListing(user=request.user, **form.cleaned_data)
            #AuctionList = AuctionsListing(user=request.user, title=Title, discription=Discription, price=Price, starting_bid=Starting_bid, image=Image, catagory=Catagory )
            # AuctionList.save()
            #print(f"{AuctionList.objects.all()}")
            context = {
                "form": ListingForm(),
                "message1":"done"
            }
            return render(request, "auctions/index.html")        
    
        else:
            context = {
                "form": ListingForm(),
                "message1":"Please Enter valid data"
            }
            return render(request, "auctions/create.html", context = context)

@login_required(login_url="auctions/login.html")
def listing(request, iduser): 
    if request.user : 
        try : 
            if WatchList.objects.get(user=request.user, ListingID=iduser) :
                added=True
        except:
            added = False
        try : 
            comments = Comment.objects.filter(listingid=iduser)
            print(comments)
        except : 
            comments = None
        try :
            current = AuctionsListing.objects.get(pk=iduser)
            if current.user == request.user:
                owner = True
            else : 
                owner = False
        except : 
            return HttpResponseRedirect(reverse("auctions:index"))
    else :
        added = False
        owner = False
    
    if current is None :
        return render("Not Found")
    else : 
        return render(request, "auctions/listing.html", {
            "current": current,
            "user" : request.user,
            "added" : added,
            "owner" : owner,
            "comments":comments,
            "bidform" : BidForm(),
            "commentform" : CommentForm()
        })
@login_required(login_url="auctions/login.html")
def watch(request, id):
    if request.method == 'POST':
        print('zizo')
        user = request.user
        WatchList.objects.create(user = user , ListingID=id)
        #print('zizo')
        return HttpResponseRedirect(reverse("auctions:listing", args=[id]))
    else:
        return HttpResponseRedirect(reverse("auctions:index"))

        
def unwatch(request, id):
    if request.user:
        try:
            w = WatchList.objects.filter(user = request.user, ListingID=id).all()
            w.delete()
            return HttpResponseRedirect(reverse("auctions:listing", args=[id]))
        except:
            return HttpResponseRedirect(reverse("auctions:listing", args=[id]))
    else:
        return HttpResponseRedirect(reverse("auctions:index"))

def watchlist(request):
    if request.user:
        try:
            obj = WatchList.objects.filter(user=request.user)
            items = []
            for i in obj:
                items.append(AuctionsListing.objects.filter(id=i.ListingID))
                print(items)
            try:
                obj = WatchList.objects.filter(user=request.user)
                count = len(obj)
            except: 
                count = None
            return render(request, "auctions/watchlisting.html", context = {
                "obj": items,
                "count": count,
            })
        except:
            try:
                w = WatchList.objects.filter(user=request.user)
                wcount=len(w)
            except:
                wcount=None
            return render(request,"auctions/watchlisting.html",{
                "obj":None,
                "count":wcount
            })
    else : 
        return HttpResponseRedirect(reverse("auctions:index"))
def bid(request, id):
    if request.method == "POST": 
        form = BidForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.cleaned_data['bid']
            try :
                starting_bid = AuctionsListing.objects.get(id=id)
                if starting_bid.starting_bid < obj :
                    starting_bid.starting_bid = obj
                    starting_bid.save()
                    bid = form.save(commit=False)
                    bid.user = request.user
                    bid.listingid = id 
                    bid.save()
                else : 
                    print("inputlargebid")
                    return render("input large bid")
                return HttpResponseRedirect(reverse("auctions:listing", args=[id]))
            except:
                return HttpResponseRedirect(reverse("auctions:index"))

def comment(request, id):
    if request.method == "POST": 
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.listingid = id
            obj.save()
            return HttpResponseRedirect(reverse("auctions:listing", args=[id]))
        else : 
            return HttpResponseRedirect(reverse("auctions:index"))
def catagories(request):
    return render()
def closebid(request, id):
    if request.user : 
        try : 
            item = AuctionsListing.objects.get(id=id)
            bid = Bid.objects.filter(listingid=id)
            #print("!")
            for i in bid :
                #print("@@")
                if i.bid == item.starting_bid : 
                    #print("@@@")
                    try : 
                        watchlist = WatchList.objects.filter(ListingId=id)
                        watchlist.delete()
                        print("done 1")
                    except :
                        pass
                    try : 
                        comment = Comment.objects.filter(listingid=id)
                        comment.delete()
                        print("done 2")
                    except:
                        pass
                    try : 
                        bid = Bid.objects.filter(listingid=id)
                        bid.delete()
                        print("done 3")
                    except:
                        pass
                    try : 
                        winner = Close()
                        winner.listingid = id 
                        winner.winner = i.user
                        winner.owner = item.user.username
                        winner.winprice = i.bid 
                        winner.save()
                        print(winner)
                        item.active = False
                        item.winner = i.user.username
                        item.save()
                        print(item.active)
                        return HttpResponseRedirect(reverse("auctions:listing", args=[id]))
                    except: 
                        pass
                
        except:
            return HttpResponseRedirect(reverse("auctions:index"))
def winnings(request):
    try :
        items = Close.objects.filter(winner=request.user)
        winnings = []
        for i in items :
            winnings.append(AuctionsListing.objects.filter(id=i.listingid))
            print(winnings)
        try: 
            obj = Close.objects.filter(winner=request.user)
            count = len(obj)
        except:
            count = None
        return render(request,"auctions/winnings.html", {
            "winnings" : winnings,
            "count" : count
        })
    except:
        try:
            c = Close.objects.filter(user=request.user)
            wcount=len(c)
        except:
            wcount=None
        return render(request,"auctions/winnings.html",{
            "winnings":None,
            "count":wcount
        })