from django.db import models
from django.conf import settings
from django.utils import timezone



class UserProfile(models.Model):
    """
    creating UserProfile model with the following features:
    1. allow the user to have only one profile 
    2. can follow and be followed by other profiles
    3. can block or be blocked by other profiles
    4. reiceve notifications from the followed profiles if needed

    """
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=20,blank=True)
    last_name =  models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to="users/images", blank=True)
    bio = models.TextField(blank=True)
    follows = models.ManyToManyField('self', through='Follow',related_name="followed_by", symmetrical=False)
    block = models.ManyToManyField('self', through='Block', related_name="blocked_by", symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.datetime.now)


    def __str__(self):
        return self.owner.email
    

    def follow(self, profile):
        Follow.objects.create(follower=self, followed = profile)

    def unfollow(self, profile):
        Follow.objects.filter(follower=self,followed=profile).delete()

    def block(self, profile):
        Block.objects.create(blocker=self, blocked=profile)

    def unblock(self, profile):
        Block.objects.filter(blocker=self, blocked=profile).delete()




class Follow(models.Model):

    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name="following")
    followed = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name="followers")
    notifications = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now=True)

    # Prevent the combination of the two fields' values from being duplicated in any other rows
    class Meta:
        unique_together = ("follower","followed")


    def __str__(self):
        return f"{self.follower.owner} follows {self.followed.owner}"

    


class Block(models.Model):
    blocker = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="blocking")
    blocked = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="blockers")
    started_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("blocker","blocked")



    def __str__(self):
        return f"{self.blocker.owner} blocks {self.blocked.owner}"
    



#-------------------------------------------------------------------------------------------------------------------------------------

# Create models for post, comments and likes
# creat a separate image model for accepting more than one image at a time for each post instance 

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    video = models.FileField(upload_to='posts/videos/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=timezone.datetime)


    class Meta:
        ordering = ['author']


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)

    def __str__(self):
        return self.post
    

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="comments")
    content = models.CharField(max_length=500)
    commented_on = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} commented on {self.commented_on}"
    



class Like(models.Model):
    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="likes")
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    done_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.author} likes {self.liked_post}"


    







