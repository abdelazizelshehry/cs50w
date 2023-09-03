from django.contrib import admin
from .models import AuctionsListing, WatchList, Bid, Comment, Close
from django.contrib.auth.models import User
# Register your models here.
admin.site.site_header = "Auction's site Administration"


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "starting_bid", "createddate")


admin.register(User)
admin.site.register(AuctionsListing, AuctionListingAdmin)
admin.site.register(WatchList)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Close)