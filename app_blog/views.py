from django.shortcuts import render,get_object_or_404, redirect
from .models import Blog
from django.utils import timezone
from .forms import BlogForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)
    page = request.GET.get('page')
    page_posts = paginator.get_page(page)
    return render(request, 'home.html',{'page_posts' : page_posts})

def detail(request,blog_id):
    blog_detail = get_object_or_404(Blog , pk=blog_id)
    return render(request,'detail.html', {'blog':blog_detail})

def new(request):
    form = BlogForm()
    return render(request,'new.html', {'form':form})

def create(request):
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid:
        form.save()

    # new_blog = Blog()
    # new_blog.title = request.POST['title']
    # new_blog.date = timezone.datetime.now()
    # new_blog.body = request.POST['body']
    # if request.FILES:
    #     new_blog.img = request.FILES['img']
    # new_blog.save()
    return redirect('home')

def edit(request,blog_id):
    edit_blog = Blog.objects.get(id=blog_id)
    form = BlogForm(instance=edit_blog)
    return render(request, 'edit.html',{'blog':edit_blog, 'form':form})

def update(request, blog_id):
    update_blog = Blog.objects.get (id = blog_id)
    form = BlogForm(request.POST, request.FILES, instance=update_blog)
    if form.is_valid:
        form.save()
    # update_blog.title = request.POST['title']
    # update_blog.body = request.POST['body']
    # update_blog.save()
    return redirect('home')

def delete(request, blog_id):
    delete_blog = Blog.objects.get(id=blog_id)
    delete_blog.delete()
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        # User has info and wants an account now!
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
               

                return redirect('login')
        else:
            return render(request, 'signup.html', {'error': 'Passwords must match'})
    else:
        # User wants to enter info
        return render(request, 'signup.html')
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return render(request,'login.html')