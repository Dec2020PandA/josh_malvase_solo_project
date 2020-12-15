from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            errors['first_name']="First name must be longer than 2 characters"
        if len(postData['last_name'])<2:
            errors['last_name']="Last name must be longer than 2 characters"
        if not email_check.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password'])<8:
            errors['password']="Password must be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw']="Password and confirm password must match"
        return errors
    def authenticate(self, email, password):
        logged_users = self.filter(email=email)
        if not logged_users:
            return False
        logged_user = logged_users[0]
        return bcrypt.checkpw(password.encode(), logged_user.password.encode())
    def profile_validator(self, postData):
        errors = {}
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])==0:
            errors['first_name'] = "First Name field cannot be left blank"
        if len(postData['last_name'])==0:
            errors['last_name']= "Last Name field cannot be left blank"
        if not email_check.match(postData['email']):
            errors['email'] = "Invalid email address!"
        return errors
    # def email_edit_validator(request, postData):
    #     email_error={}
    #     to_check = User.objects.filter(email=postData['email'])
    #     if len(to_check)>0:
    #         print(to_check)
    #         email_error['reg_email'] = "Email is already registered"
    #     return email_error


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    date_of_birth = models.DateField(max_length=8, default="1930-01-01")
    password = models.CharField(max_length=255)
    prof_photo = models.ImageField(upload_to='media/', null=True)
    about = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors = {}
        if len(postData['content'])<1:
            errors['content']="Message cannot be blank!"
        return errors 

class Message(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name="liked_messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class BottleManager(models.Manager):
    def bottle_validator(self, postData):
        errors = {}
        if len(postData['classification'])<1:
            errors['classification']="Classification cannot be left blank. If unknown, enter N/A"
        if len(postData['vintage'])<1:
            errors['vintage']="Vintage cannot be left blank. If unknown, enter N/A"
        if len(postData['varietal'])<1:
            errors['varietal']="Varietal cannot be left blank. If unknown, enter N/A"
        if len(postData['producer'])<1:
            errors['producer']="Producer cannot be left blank. If unknown, enter N/A"
        return errors

class Bottle(models.Model):
    classification = models.CharField(max_length=20)
    vintage = models.CharField(max_length=6)
    varietal = models.CharField(max_length=100)
    producer = models.CharField(max_length=250)
    tasting_notes = models.TextField()
    bottle_photo = models.ImageField(upload_to='media/', null=True)
    owner = models.ForeignKey(User, related_name="bottles", on_delete=models.CASCADE)
    objects = BottleManager()

class Comment(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

