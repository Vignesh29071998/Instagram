from django.db import models


class SignUp(models.Model):
    Username = models.CharField(max_length = 20)
    Password = models.CharField(max_length = 20)
    Number = models.PositiveIntegerField()
    Email = models.EmailField()
    Image = models.ImageField(upload_to='images/',default="default.jpg",blank=True)
    
    def __str__(self):
        return self.Username
class Posts(models.Model):
    User = models.ForeignKey(SignUp,on_delete=models.CASCADE,default=None)
    Tweet = models.TextField(default=None,blank=True,null=True)
    Date = models.DateTimeField(auto_now_add=True)
    Profile = models.ImageField(default=None,blank=True,null=True)
    Posts_image = models.ImageField(default=None,blank=True,null=True)
    Posts_video = models.FileField(default=None,blank=True,null=True)
     
    def __str__(self):
        return self.User.Username
class FriendList(models.Model):
    Friend = models.ForeignKey(SignUp,on_delete=models.CASCADE,default=None)
    Friend_name = models.CharField(max_length=30,default=None,blank=True)
    Status = models.CharField(max_length=20,default=None,blank=True,null=True)