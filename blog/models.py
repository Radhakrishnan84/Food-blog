from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/')
    category = models.CharField(max_length=100)

    cooking_time = models.IntegerField()
    difficulty = models.CharField(max_length=50)
    rating = models.FloatField(default=4.5)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='blogs/')
    description = models.TextField()
    cooking_time = models.CharField(max_length=50, default="15 min")
    author = models.CharField(max_length=100, default="chef")
    created_at = models.DateTimeField(auto_now_add=True)
    ingredients = models.TextField(blank=True)
    steps = models.TextField(blank=True)
    tags = models.CharField(max_length=200, blank=True)
    allow_comments = models.BooleanField(default=True)

    status = models.CharField(
    max_length=10,
    choices=(('draft','Draft'),('published','Published')),
    default='published'
)

    def __str__(self):
        return self.title
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'blog')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class BlogStep(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='steps/', blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.blog.title} - Step {self.order}"


class BlogImage(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return self.blog.title