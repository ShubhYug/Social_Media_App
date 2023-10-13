from django.db import models
from django.contrib.auth.models import User

# Create your models here.
RELATIONSHIP_CHOICE = (
    ('Singel', 'Singel'),
    ('Married', 'Married'),
    ('Try to SHADi', 'Try to SHADi'),
)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)   # when we will delete user then


    # profile_image = models.FileField(upload_to='profile/', null=True )
    bio = models.TextField(max_length=100,blank=True)
    work = models.CharField(max_length=100,blank=True)
    education = models.CharField(max_length=100,blank=True)
    hobbies = models.TextField(blank=True)
    link = models.URLField(blank=True)
    profile_image = models.FileField(upload_to='profile/',blank=True)
    relationship = models.CharField(max_length=15, choices=RELATIONSHIP_CHOICE,blank=True)
    followers = models.PositiveIntegerField(default=0)
    contact = models.CharField(max_length=12, null=True)
    following = models.PositiveIntegerField(default=0)
    follows = models.ManyToManyField("self",related_name="followed_by",symmetrical=False,blank=True)

    class Meta:
        db_table = 'Profile'

    def __str__(self):
        return self.user.username
        # return self.user.username, self.contact,self.bio,self.hobbies

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_image = models.FileField(upload_to='post/', null=True )


    class Meta:
        db_table = 'Post'

    def __str__(self):
        return self.id,self.user,self.content,self.created_at,self.post_image
        # return self.user,self.id

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comment'    

    def __str__(self):
        # return self.user, self.post, self.text, self.created_at
        return f"{self.user.username} - {self.post.text} - {self.created_at} - {self.post}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Like'

class Friendship(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=20, default='pending')  # 'pending', 'accepted', 'rejected'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Friendship'

    def __str__(self):
        return self.sender, self.status
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='requests_received', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def _str_(self):
        return f'{self.from_user} : {self.to_user}'

    class Meta:
        db_table = 'FriendRequest'

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)