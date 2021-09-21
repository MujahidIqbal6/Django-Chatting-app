from django.db import models

# Create your models here.

class User(models.Model):
    user_name=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    active=models.BooleanField(default=False)

    def __str__(self):
        return self.user_name

class Mesg(models.Model):
    msg_text=models.CharField(max_length=400)
    is_read=models.BooleanField(default=True)
    from_user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='sentfrom',default=1)
    to_user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='sentto',default=1)

    def __str__(self):
        return self.msg_text

    