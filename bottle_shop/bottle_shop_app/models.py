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


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()