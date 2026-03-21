from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Recipe
from .models import Blog
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Like, Comment
from .models import BlogStep, BlogImage
from django.shortcuts import render, get_object_or_404



def home(request):

    recipes = Recipe.objects.all().order_by('-created_at')[:3]
    blogs = Blog.objects.all().order_by('-created_at')[:4]

    return render(request, 'index.html', {
        'recipes': recipes,
        'blogs': blogs
    })



def blog_page(request):

    category = request.GET.get('category')

    blogs = Blog.objects.all().order_by('-created_at')

    blogs = Blog.objects.filter(status='published')

    if category:
        blogs = blogs.filter(category=category)

    # PAGINATION
    paginator = Paginator(blogs, 4)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    # CATEGORY COUNT
    categories = Blog.objects.values('category')\
        .annotate(count=Count('id'))

    return render(request, 'blog.html', {
        'blogs': blogs,
        'categories': categories,
        'selected_category': category
    })

    
def blog_detail(request, id):
    blog = Blog.objects.get(id=id)

    steps = BlogStep.objects.filter(blog=blog).order_by('order')
    gallery = BlogImage.objects.filter(blog=blog)[:5]

    ingredients = blog.ingredients.split(",") if hasattr(blog, 'ingredients') and blog.ingredients else []

    context = {
        'blog': blog,
        'steps': steps,
        'gallery': gallery,
        'ingredients': ingredients,
    }

    return render(request, 'blog_detail.html', context)


def recipes_page(request):
    
    recipes = Recipe.objects.all().order_by('-created_at')[:3]

    return render(request, 'recipes.html', {
        'recipes': recipes,
    })

  


@login_required
def create_blog(request):

    if request.method == "POST":

        action = request.POST.get("action")

        ingredients = request.POST.getlist("ingredients")
        steps = request.POST.getlist("steps")

        blog = Blog.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            image=request.FILES.get("image"),
            category=request.POST.get("category"),
            cooking_time=request.POST.get("cook_time"),
            ingredients=",".join(ingredients),
            steps=",".join(steps),
            tags=request.POST.get("tags"),
            allow_comments=True if request.POST.get("allow_comments") else False,
            status='draft' if action == 'draft' else 'published'
        )
           # AFTER saving blog
        steps = request.POST.getlist("steps")
        step_images = request.FILES.getlist("step_images")

        for i, step in enumerate(steps):
             BlogStep.objects.create(
               blog=blog,
               description=step,
        image=step_images[i] if i < len(step_images) else None,
        order=i
    )

# GALLERY IMAGES (MAX 5)
        gallery_images = request.FILES.getlist("gallery_images")[:5]
        
        for img in gallery_images:
             BlogImage.objects.create(blog=blog, image=img)

        return redirect('dashboard')

    return render(request, 'write_blog.html')

        


@login_required
def toggle_like(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    like, created = Like.objects.get_or_create(user=request.user, blog=blog)

    if not created:
        like.delete()

    return redirect('home')


def add_comment(request, blog_id):
    if request.method == "POST":
        text = request.POST.get('comment')

        Comment.objects.create(
            user=request.user,
            blog_id=blog_id,
            text=text
        )

    return redirect('home')