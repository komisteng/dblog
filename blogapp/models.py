from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    birth = models.CharField(max_length=10)
    mail = models.CharField(max_length=100)
    gender_choices = (
        (0, '不愿意透露'),
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(choices=gender_choices, default=0)
    bilibili_id = models.CharField(max_length=16)
    is_admin = (
        (0,"False"),
        (1,"True")
    )
    admin = models.SmallIntegerField(choices=is_admin,default=0)
    register_date = models.DateTimeField(auto_now_add=True)

class Blog(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    final_edited_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    body = models.TextField()