from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        # password2 = extra_fields.pop('password2', None)
        # print(password2)
        # print("VIvek")
        if not username:
            raise ValueError("The Username field must be set")
        print(extra_fields)
        email = extra_fields.pop('email',None)
        if email:
            email = self.normalize_email(email)
            print(email)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def update(self,username, email, phone_number,password,first_name,last_name):
        """Updates an existing user object."""
        print("hello")
        user = self.get(username=username)
        print(password)
        user.set_password(password)
        print(user['password'])
        user.save()
        return user
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
    
class User(AbstractUser):
    # Add custom fields here
    email = models.EmailField(max_length=255,unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    def __str__(self) -> str:
        return self.username

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body
