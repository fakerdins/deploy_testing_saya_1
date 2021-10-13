from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post', null=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title + ' | ' + str(self.author)


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    likes = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.likes)


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return str(self.image)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment)


class Rating(models.Model):
    RATE = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5")
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating', null=True)
    ratings = models.CharField(choices=RATE, max_length=1, default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rating')

    def __str__(self):
        return f"{self.post} | {self.ratings}"







