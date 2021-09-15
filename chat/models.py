from django.db import models

# Create your models here.

class User(models.Model):
    user_name=models.CharField(max_length=200)
    password=models.CharField(max_length=200)

    def __str__(self):
        return self.user_name

class Mesg(models.Model):
    msg_text=models.CharField(max_length=400)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.msg_text
