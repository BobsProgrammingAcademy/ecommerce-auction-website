from decimal import Decimal
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Auction, Bid, Category, Image, User
from .forms import AuctionForm, ImageForm, CommentForm, BidForm


def index(request):
    '''
    The default route which renders a Dashboard page
    '''
    auctions = Auction.objects.all()

    expensive_auctions = Auction.objects.order_by('-starting_bid')[:4]

    for auction in auctions:
        auction.image = auction.get_images.first()

    # Show 5 auctions per page
    page = request.GET.get('page', 1)
    paginator = Paginator(auctions, 5)

    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'categories': Category.objects.all(),
        'auctions': auctions,
        'expensive_auctions': expensive_auctions,
        'auctions_count': Auction.objects.all().count(),
        'bids_count': Bid.objects.all().count(),
        'categories_count': Category.objects.all().count(),
        'users_count': User.objects.all().count(),
        'pages': pages,
        'title': 'Dashboard',
    })


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'register.html', {
                'message': 'Passwords must match.',
                'title': 'Register',
                'categories': Category.objects.all()
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username already taken.',
                'title': 'Register',
                'categories': Category.objects.all()
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'register.html', {
            'title': 'Register',
            'categories': Category.objects.all()
        })


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {
                'message': 'Invalid username and/or password.',
                'title': 'Log in',
                'categories': Category.objects.all()
            })
    else:
        return render(request, 'login.html', {
            'title': 'Log in',
            'categories': Category.objects.all()
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def auction_create(request):
    '''
    It allows the user to create a new auction
    '''
    ImageFormSet = forms.modelformset_factory(Image, form=ImageForm, extra=2)

    if request.method == 'POST':
        auction_form = AuctionForm(request.POST, request.FILES)
        image_form = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if auction_form.is_valid() and image_form.is_valid():
            new_auction = auction_form.save(commit=False)
            new_auction.creator = request.user
            new_auction.save()

            for auction_form in image_form.cleaned_data:
                if auction_form:
                    image = auction_form['image']

                    new_image = Image(auction=new_auction, image=image)
                    new_image.save()

            return render(request, 'auction_create.html', {
                'categories': Category.objects.all(),
                'auction_form': AuctionForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
                'title': 'Create Auction',
                'success': True
            })
        else:
            return render(request, 'auction_create.html', {
                'categories': Category.objects.all(),
                'auction_form': AuctionForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
                'title': 'Create Auction',
            })
    else:
        return render(request, 'auction_create.html', {
            'categories': Category.objects.all(),
            'auction_form': AuctionForm(),
            'image_form': ImageFormSet(queryset=Image.objects.none()),
            'title': 'Create Auction',
        })


def active_auctions_view(request):
    '''
    It renders a page that displays all of
    the currently active auction listings
    Active auctions are paginated: 3 per page
    '''
    category_name = request.GET.get('category_name', None)
    if category_name is not None:
        auctions = Auction.objects.filter(active=True, category=category_name)
    else:
        auctions = Auction.objects.filter(active=True)

    for auction in auctions:
        auction.image = auction.get_images.first()
        if request.user in auction.watchers.all():
            auction.is_watched = True
        else:
            auction.is_watched = False

    # Show 3 active auctions per page
    page = request.GET.get('page', 1)
    paginator = Paginator(auctions, 3)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'auctions_active.html', {
        'categories': Category.objects.all(),
        'auctions': auctions,
        'auctions_count': auctions.count(),
        'pages': pages,
        'title': 'Active Auctions'
    })


@login_required
def watchlist_view(request):
    '''
    It renders a page that displays all of
    the listings that a user has added to their watchlist
    Auctions are paginated: 3 per page
    '''
    auctions = request.user.watchlist.all()

    for auction in auctions:
        auction.image = auction.get_images.first()

        if request.user in auction.watchers.all():
            auction.is_watched = True
        else:
            auction.is_watched = False

    # Show 3 active auctions per page
    page = request.GET.get('page', 1)
    paginator = Paginator(auctions, 3)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'auctions_active.html', {
        'categories': Category.objects.all(),
        'auctions': auctions,
        'auctions_count': auctions.count(),
        'pages': pages,
        'title': 'Watchlist'
    })


@login_required
def watchlist_edit(request, auction_id, reverse_method):
    '''
    It allows the users to edit the watchlist -
    add and remove items from the Watchlist
    '''
    auction = Auction.objects.get(id=auction_id)

    if request.user in auction.watchers.all():
        auction.watchers.remove(request.user)
    else:
        auction.watchers.add(request.user)

    if reverse_method == 'auction_details_view':
        return auction_details_view(request, auction_id)
    else:
        return HttpResponseRedirect(reverse(reverse_method))


def auction_details_view(request, auction_id):
    '''
    It renders a page that displays the details of a selected auction
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    auction = Auction.objects.get(id=auction_id)

    if request.user in auction.watchers.all():
        auction.is_watched = True
    else:
        auction.is_watched = False

    return render(request, 'auction.html', {
        'categories': Category.objects.all(),
        'auction': auction,
        'images': auction.get_images.all(),
        'bid_form': BidForm(),
        'comments': auction.get_comments.all(),
        'comment_form': CommentForm(),
        'title': 'Auction'
    })


@login_required
def auction_bid(request, auction_id):
    '''
    It allows the signed in users to bid on the item
    '''
    auction = Auction.objects.get(id=auction_id)
    amount = Decimal(request.POST['amount'])

    if amount >= auction.starting_bid and (auction.current_bid is None or amount > auction.current_bid):
        auction.current_bid = amount
        form = BidForm(request.POST)
        new_bid = form.save(commit=False)
        new_bid.auction = auction
        new_bid.user = request.user
        new_bid.save()
        auction.save()

        return HttpResponseRedirect(reverse('auction_details_view', args=[auction_id]))
    else:
        return render(request, 'auction.html', {
            'categories': Category.objects.all(),
            'auction': auction,
            'images': auction.get_images.all(),
            'form': BidForm(),
            'error_min_value': True,
            'title': 'Auction'
        })


def auction_close(request, auction_id):
    '''
    It allows the signed in user who created the listing
    to “close” the auction, which makes the highest bidder
    the winner of the auction and makes the listing no longer active
    '''
    auction = Auction.objects.get(id=auction_id)

    if request.user == auction.creator:
        auction.active = False
        auction.buyer = Bid.objects.filter(auction=auction).last().user
        auction.save()

        return HttpResponseRedirect(reverse('auction_details_view', args=[auction_id]))
    else:
        auction.watchers.add(request.user)

        return HttpResponseRedirect(reverse('watchlist_view'))


def auction_comment(request, auction_id):
    '''
    It allows the signed in users to add comments to the listing page
    '''
    auction = Auction.objects.get(id=auction_id)
    form = CommentForm(request.POST)
    new_comment = form.save(commit=False)
    new_comment.user = request.user
    new_comment.auction = auction
    new_comment.save()
    return HttpResponseRedirect(reverse('auction_details_view', args=[auction_id]))


def category_details_view(request, category_name):
    '''
    Clicking on the name of any category takes the user to a page that
    displays all of the active listings in that category
    Auctions are paginated: 3 per page
    '''
    category = Category.objects.get(category_name=category_name)
    auctions = Auction.objects.filter(category=category)

    for auction in auctions:
        auction.image = auction.get_images.first()

    # Show 3 active auctions per page
    page = request.GET.get('page', 1)
    paginator = Paginator(auctions, 3)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'auctions_category.html', {
        'categories': Category.objects.all(),
        'auctions': auctions,
        'auctions_count': auctions.count(),
        'pages': pages,
        'title': category.category_name
    })
