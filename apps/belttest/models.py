from __future__ import unicode_literals
from datetime import datetime, date
import bcrypt

from django.db import models

class UserManager(models.Manager):
    def login(self, post):
        user_list = User.objects.filter(username=post['username'])
        if user_list:
            user = user_list[0]
            #check their credentials
            if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password:
                #then login is valid
                return user
        #else:
        return None

    def register(self, post):
        encrypted_password = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
        User.objects.create(name=post['name'], username=post['username'], password=encrypted_password, date_hired=post['date_hired'])

    def validate_user_info(self, post):
        errors = []

        if len(post['name']) < 3:
            errors.append('Name must contain at least 3 characters!')
        # if not post['firstname'].isalpha():
        #     errors.append('All First Name characters must be alphabetic!.')
        if len(post['username']) == 0:
            errors.append('Username cannot be blank!')

        if len(post['password']) < 8:
            errors.append('Your password must contain at least 8 characters!')
        if post['password'] != post['confpass']:
            errors.append('Your confirmation password must match your password!')
        elif post['password'] != post['confpass']:
            errors.append("Password and confirmation filed must match")

        return errors

class WishManager(models.Manager):
    def check_form_data(self, form):
        errors = []
        if not form ['item']:
            errors.append("An item is required")
        if len(form['item']) < 3:
            errors.append("Your item must contain at least 3 characters")
        return errors




# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=250)
    confirm_password = models.CharField(max_length=250)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Wish(models.Model):
    #the joiner:
    users = models.ManyToManyField(User, related_name='wishes')
    #the planner:
    user_wish = models.ForeignKey(User)
    item = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = WishManager()
