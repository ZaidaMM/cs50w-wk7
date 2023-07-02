from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.all().order_by('id').reverse()

    # Pagination, show 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        'posts': posts,
        'page_obj': page_obj
    })

def compose(request):
    if request.method == 'POST':
        body = request.POST['compose-body']
        user = User.objects.get(pk=request.user.id)
        post = Post(body = body, author = user)
        post.save()

        return HttpResponseRedirect(reverse('index'))
    
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    # Filter posts by user
    posts = Post.objects.filter(author=user).order_by('id').reverse()
    following = Follow.objects.filter(follower=user)
    followers = Follow.objects.filter(following=user)

    try:
        isFollower = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(isFollower) != 0:
            isFollowing = False
        else:
            isFollowing = True
    except:
        isFollowing = False

    # Pagination, show 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/profile.html", {
        'posts': posts,
        'page_obj': page_obj,
        'username': user.username,
        'followers': followers,
        'following': following,
        'isFollowing': isFollowing,
        'profile_owner': user
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def following(request):
    current_user = User.objects.get(pk=request.user.id)
    followingUsers = Follow.objects.filter(follower=current_user)
    posts = Post.objects.all().order_by('id').reverse()

    followingPosts = []

    for post in posts:
        for person in followingUsers:
            if person.following == post.author:
                followingPosts.append(post)


# Pagination, show 10 posts per page
    paginator = Paginator(followingPosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        'page_obj': page_obj
    })   


def follow(request):
   follower_user = request.POST['followerUser']
   current_user = User.objects.get(pk=request.user.id)
   follower_user_content = User.objects.get(username=follower_user)

   foll = Follow(follower=current_user, following=follower_user_content)
   foll.save()

   user_id = follower_user_content.id
   return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


    

def unfollow(request):
   follower_user = request.POST['followerUser']
   current_user = User.objects.get(pk=request.user.id)
   follower_user_content = User.objects.get(username=follower_user)

   foll = Follow.objects.get(follower=current_user, following=follower_user_content)
   foll.delete()

   user_id = follower_user_content.id
   return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))