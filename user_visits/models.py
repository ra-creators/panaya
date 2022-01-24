from django.db import models

# Create your models here.
class HomeCount(models.Model):
    count = models.IntegerField()
    created = models.DateTimeField()

    def increase_count(self):
        self.count += 1
        self.save()

    def get_count(self):
        return self.count

class CartCount(models.Model):
    count = models.IntegerField()
    created = models.DateTimeField()

    def increase_count(self):
        self.count += 1 
        self.save()

    def get_count(self):
        return self.count

class BlogCount(models.Model):
    count = models.IntegerField()
    created = models.DateTimeField()

    def increase_count(self):
        self.count += 1 
        self.save()

    def get_count(self):
        return self.count