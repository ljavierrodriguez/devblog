from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatars', blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    github = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='posts')
    title = models.CharField(max_length=200, blank=False, null=False, unique=True)
    slug = models.SlugField(blank=True)
    resume = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now=timezone.now)
    image = models.ImageField(upload_to='images/posts', blank=True, null=True, default='images/posts/placeholder.png')

    def save(self, *args,**kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='portfolio')
    image = models.ImageField(upload_to='images/works')
    skills = models.CharField(max_length=200, blank=False, null=False)
    duration = models.CharField(max_length=200, blank=False, null=False)
    cost = models.FloatField()
    url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.skills
