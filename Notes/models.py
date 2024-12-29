from django.db import models

from django.contrib.auth.models import User

# Create your models here

class Signup(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    contact=models.CharField(max_length=15,null=True)
    branch=models.CharField(max_length=40)
    designation=models.CharField(max_length=10,default='student')

    def __str__(self):
        return self.user.username


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploadingdate= models.DateField(auto_now_add=True)
    branch = models.CharField(max_length=40)
    subject=models.CharField(max_length=40)
    designation=models.CharField(max_length=40,default="student")
    notesFile= models.FileField(null=True)
    filetype=models.CharField(max_length=40)
    description= models.CharField(max_length=200,null=True)
    status=models.CharField(max_length=40)
    semester=models.CharField(max_length=50,default="unknown")


    def __str__(self):
        return self.user.username