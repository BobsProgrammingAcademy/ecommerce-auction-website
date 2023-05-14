from django.contrib import admin

from .models import Auction, Image, Bid, Comment, Category, User

admin.site.register(Auction)
admin.site.register(Image)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(User)
