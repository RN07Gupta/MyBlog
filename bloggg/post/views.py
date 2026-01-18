from datetime import date
import email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Post
from django.utils.dateparse import parse_datetime



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  # ✅ FIXED

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "post/signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "post/signup.html")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect('loginn')

    return render(request, 'post/signup.html')



def loginn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'post/loginn.html')



@login_required(login_url='loginn')
def base(request):
    if request.method == "POST":
        Post.objects.create(
            title=request.POST.get("title"),
            content=request.POST.get("content"),
            author=request.user
        )
        return redirect("base")

    # 🔹 Only OTHER users' posts (Community)
    all_posts = Post.objects.exclude(author=request.user).order_by('-created_at')

    # 🔹 Only logged-in user's posts (Dashboard)
    my_posts = Post.objects.filter(author=request.user).order_by('-created_at')

    return render(
        request,
        "post/base.html",
        {
            "all_posts": all_posts,
            "my_posts": my_posts
        }
    )

def out(request):
    return render(request, 'post/loginn.html')

def landing(request):
    return render(request, 'post/landing.html')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('base')


    
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect("base")

    return render(request, "post/edit_post.html", {"post": post})


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by("-created_at")

    return render(request, "post/profile.html", {
        "profile_user": user,
        "posts": posts
    })
    
    

