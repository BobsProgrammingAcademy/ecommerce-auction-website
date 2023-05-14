from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('auction/create', views.auction_create, name='auction_create'),
    path('auction/active', views.active_auctions_view, name='active_auctions_view'),
    path('auction/active/<str:category_name>', views.active_auctions_view, name='active_auctions_view'),
    path('auction/watchlist', views.watchlist_view, name='watchlist_view'),
    path('auction/watchlist/<int:auction_id>/edit/<str:reverse_method>', views.watchlist_edit, name='watchlist_edit'),
    path('auction/<str:auction_id>', views.auction_details_view, name='auction_details_view'),
    path('auction/<str:auction_id>/bid', views.auction_bid, name='auction_bid'),
    path('auction/<str:auction_id>/close', views.auction_close, name='auction_close'),
    path('auction/<str:auction_id>/comment', views.auction_comment, name='auction_comment'),
    path('categories/<str:category_name>', views.category_details_view, name='category_details_view'),
]
