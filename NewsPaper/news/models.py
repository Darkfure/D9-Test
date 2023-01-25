from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self, posts_rate, comments_rate, comments_to_posts):
        self.posts_rate = posts_rate
        self.comments_rate = comments_rate
        self.comments_to_posts = comments_to_posts

        self.rating = posts_rate*3 + comments_rate + comments_to_posts
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return self.name.title()


class UserCategory(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



article = 'AR'
news = 'NW'

TYPES = [
    (article, 'Статья'),
    (news, 'Новость'),
]


class Post(models.Model):
    heading = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2,
                            choices=TYPES)
    create_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    category = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.create_time} {self.heading.title()}: {self.text[:20]}...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def preview(self):
        prev = self.text[:123]
        return f'{prev}...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)


class Comment(models.Model):
    text = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()






