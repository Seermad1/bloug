from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, User, Topic
from django.db.models import Q
from .forms import PostForm, MyUserCreationForm, UpdateUser
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.


def login_user(request):

    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "password incorrect.")
        except:
            messages.error(request, 'User does not exist.')

    context = {"page": page}
    return render(request, "blog/login_register.html", context)


def logout_user(request):
    logout(request)
    return redirect("home")


def register_user(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "email taken")
                else:
                    if User.objects.filter(username=username).exists():
                       messages.error(request, "username taken") 
                    else:
                        user = User.objects.create_user(
                            username=username, email=email, password=password
                        )
                        user.save()
                        login(request, user)
                        return redirect("home")
        else:
            messages.error(request, "password donot match.")
    # form = MyUserCreationForm()
    # if request.method == "POST":
    #     form = MyUserCreationForm(request.POST)
    #     try:
    #         if form.is_valid:
    #             user = form.save(commit=False)
    #             user.username = user.username.lower()
    #             user.save()
    #             login(request, user)
    #             return redirect("home")
    #     except:
    #         messages.error(request, "An error occurred during registration.")

    context = {}
    return render(request, "blog/login_register.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    posts = Post.objects.filter(Q(title__icontains=q) |
                                Q(author__username__icontains=q)|
                               Q(topics__name__icontains=q) )
    paginator  = Paginator(posts,4)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    topics = Topic.objects.all()
    context = {"page_obj": page_obj, "topics":topics}
    return render(request, "blog/home.html", context)


def blog_post(request, pk):
    post = Post.objects.get(id=pk)
    post_comments = post.comment_set.all()
    if request.method == "POST":
        Comment.objects.create(
            user=request.user,
            post=post,
            comment=request.POST.get("comment")
        )
        return redirect("post", pk=post.id)
    context = {"post": post, "post_comments": post_comments}
    return render(request, "blog/post.html", context)


@login_required(login_url="login")
def create_post(request):
    page = "create_post"
    form = PostForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("tag_name")
        if Topic.objects.filter(name=topic_name).exists():
            topic = Topic.objects.get(name=topic_name)
        else:
            topic = Topic.objects.create(name=topic_name)
        Post.objects.create(
            author=request.user,
            title=request.POST.get("title"),
            body=request.POST.get("body"),
            topics=topic,
            post_image=request.FILES.get("post_image")
        )
        return redirect("home")
        # form = PostForm(request.POST, request.FILES)
        # if form.is_valid:
        #     form.save()
        #     return redirect("home")
    context = {"topics":topics, "form":form, "page":page}
    return render(request, "blog/create_post.html", context)


def update_post(request, pk):
    post = Post.objects.get(id=pk)

    form = PostForm(instance=post)
    if request.method == "POST":
        topic_name = request.POST.get("topic")

        if Topic.objects.filter(name=topic_name).exists():
            topic = Topic.objects.get(name=topic_name)
        else:
            topic = Topic.objects.create(name=topic_name)

        post.title = request.POST["title"]
        post.author = request.user
        post.body = request.POST["body"]
        post.topics = topic

        if request.FILES.get("post_image") == None:
            post.post_image = post.post_image
        else:
            post.post_image = request.FILES.get("post_image")
        post.save()
        return redirect("home")
        # form = PostForm(request.POST, request.FILES, instance=post)
        # if form.is_valid:
        #     form.save()
        #     return redirect("home")
    context = {"form":form}
    return render(request, "blog/create_post.html", context)


def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        post.delete()
        return redirect("profile", post.author.id)
    context = {"post": post}
    return render(request, "blog/delete.html", context)


def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == "POST":
        comment.delete()
        return redirect("home")

    context = {"post": comment}
    return render(request, "blog/delete.html", context)

@login_required(login_url="login")
def profile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()[0:4]
    context = {"user": user, "posts": posts}
    return render(request, "blog/profile.html", context)

@login_required(login_url="login")
def update_profile(request):
    user = request.user
    form = UpdateUser(instance=user)
    if request.method == "POST":
        form = UpdateUser(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", user.id)
    context = {"form":form}
    return render(request, "blog/updateUser.html", context)


def about(request):
    return render(request, "blog/about.html")