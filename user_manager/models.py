from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserProfileManager(BaseUserManager):
    """Manages the user profiles"""
    def create_user(self, email, fname, lname, dob, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, fname=fname, lname=lname, dob=dob)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fname, lname, dob, password=None):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, fname, lname, dob, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Database models for users (Making a completely different user model)"""
    email = models.EmailField(max_length=255, unique=True)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    dob = models.DateField()
    otp = models.IntegerField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)  
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname', 'dob']

    def get_full_name(self):
        return self.fname + " " + self.lname
    
    def get_email(self):
        return self.email

    def get_dob(self):
        return self.dob
    
    def __str__(self):
        return self.email

