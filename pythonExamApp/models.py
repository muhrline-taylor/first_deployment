from django.db import models
import re
from datetime import date

class UserManager(models.Manager):
    def registerValidator(self, postData):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['form_fname_register']) < 3:
            errors['no_fname_error1'] = "Enter your first name!"
        if len(postData['form_lname_register']) < 3:
            errors['no_lname_error1'] = "Enter your last name!"
        if not email_regex.match(postData['form_email_register']):
            errors['invalid_email_error'] = "Invalid email address!"
        if len(postData['form_pw1_register']) < 8:
            errors['pw1_error1'] = "Password must be at least 8 characters!"
        if postData['form_pw1_register'] != postData['form_pw2_register']:
            errors['pw_not_confirmed'] = "Password fields must be identical!"
        return errors

    def loginValidator(self, postData):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData['form_email_login']):
            errors['invalid_email_error2'] = "Invalid email address!"
            return errors
        user_email = postData['form_email_login']
        user_pw = postData['form_pw_login']
        temp = User.objects.filter(email=user_email)
        temp2 = User.objects.filter(email=user_email, password=user_pw)
        if len(temp) == 0:
            errors['unregistered_email'] = "Email is not yet registered!"
            return errors
        elif len(temp2) == 0:
            errors['incorrect_pw'] = "Incorrect password!"
            return errors
        if len(postData['form_pw_login']) < 8:
            errors['invalid_pw_error1'] = "Invalid password!"
        return errors

class TripManager(models.Manager):
    def tripValidator(self, postData):
        errors = {}
        dateToday = date.today()
        print(postData['trip_start_register'])
        print(dateToday)
        print("LOOK HERE    ^^^^^     LOOK HERE")
        if len(postData['trip_destination_register']) == 0:
            errors['empty_dest_error'] = "Destination cannot be blank!"
        if len(postData['trip_description_register']) == 0:
            errors['empty_desc_error'] = "Description cannot be blank!"
        if len(postData['trip_start_register']) == 0:
            errors['empty_start_error'] = "Start date cannot be blank!"
        if len(postData['trip_end_register']) == 0:
            errors['empty_end_error'] = "End date cannot be blank!"
        elif postData['trip_end_register'] < str(dateToday):
            errors['trip_over_error'] = "End date cannot be in the past!"
        if postData['trip_start_register'] < str(dateToday):
            errors['ongoing_trip_error'] = "Start date cannot be in the past!"
        elif postData['trip_start_register'] > postData['trip_end_register']:
            errors['negative_trip_error'] = "End date cannot come before start date!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    travellers = models.ManyToManyField(User, related_name="trips_planned")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
