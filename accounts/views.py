from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.contrib.auth.decorators import login_required
from blog.models import Blog
from .models import AccountProfile


# LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # LOGIN WITH EMAIL OR USERNAME
        user_obj = User.objects.filter(email=username).first()
        if user_obj:
            username = user_obj.username

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # ADMIN REDIRECT
            if user.is_superuser:
                return redirect('/admin/')

            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# REGISTER


def register_view(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        # EMAIL VALIDATION
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Enter a valid email address")
            return redirect('register')

        # CHECK EXISTING USER
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        # PASSWORD VALIDATION
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('register')

        if not re.search(r"[A-Z]", password):
            messages.error(request, "Password must contain at least 1 uppercase letter")
            return redirect('register')

        if not re.search(r"[a-z]", password):
            messages.error(request, "Password must contain at least 1 lowercase letter")
            return redirect('register')

        if not re.search(r"[0-9]", password):
            messages.error(request, "Password must contain at least 1 number")
            return redirect('register')

        # ✅ CREATE USER (EMAIL AS USERNAME)
        user = User.objects.create_user(
            username=email,   # IMPORTANT (Django requires username)
            email=email,
            password=password
        )

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('dashboard')

    return render(request, 'register.html')



@login_required
def dashboard(request):
    from blog.models import Blog

    profile, _ = AccountProfile.objects.get_or_create(user=request.user)

    # UPDATE PROFILE
    if request.method == "POST":

        # 🔥 HANDLE IMAGE UPLOAD (SAFE)
        if request.FILES.get('image'):
            image = request.FILES['image']

            # ✅ VALIDATE FILE TYPE
            if image.content_type.startswith('image/'):
                profile.image = image
            else:
                from django.contrib import messages
                messages.error(request, "Only image files are allowed")
                return redirect('dashboard')

        # ✅ UPDATE TEXT FIELDS (SAFE DEFAULTS)
        profile.bio = request.POST.get('bio') or profile.bio
        profile.location = request.POST.get('location') or profile.location

        if request.method == "POST":

    # 🔥 REMOVE PROFILE LOGIC
         if request.POST.get('remove_profile'):

        # delete image
          if profile.image:
            profile.image.delete(save=False)

        # reset fields
        profile.image = None
        profile.bio = ""
        profile.location = ""

        profile.save()

        from django.contrib import messages
        messages.success(request, "Profile updated successfully")

        return redirect('dashboard')  # 🔥 prevents form resubmit

    # FETCH DATA
    blogs = Blog.objects.filter(user=request.user, status='published')
    drafts = Blog.objects.filter(user=request.user, status='draft')

    context = {
        'profile': profile,
        'blogs': blogs,
        'blog_count': blogs.count(),
        'draft_count': drafts.count(),
    }

    return render(request, 'dashboard.html', context)


@login_required
def unpublish_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id, user=request.user)
    blog.status = 'draft'
    blog.save()
    return redirect('dashboard')


@login_required
def publish_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id, user=request.user)
    blog.status = 'published'
    blog.save()
    return redirect('dashboard')




@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, user=request.user)

    if request.method == "POST":

        blog.title = request.POST.get('title')
        blog.description = request.POST.get('description')
        blog.category = request.POST.get('category')
        blog.cooking_time = request.POST.get('cooking_time')

        # OPTIONAL FIELDS
        blog.ingredients = request.POST.get('ingredients')
        blog.steps = request.POST.get('steps')
        blog.tags = request.POST.get('tags')

        # IMAGE UPDATE
        if request.FILES.get('image'):
            blog.image = request.FILES['image']

        # ACTION (PUBLISH / DRAFT)
        action = request.POST.get('action')

        if action == "publish":
            blog.status = "published"
        else:
            blog.status = "draft"

        blog.save()
        

        return redirect('dashboard')

    return render(request, 'edit_blog.html', {'blog': blog})


# LOGOUT
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

