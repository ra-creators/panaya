from django.db import models

# Create your models here.
class ConnectEmails(models.Model):
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'ConnectUsEmails'

class ConnectUs(models.Model):
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=255)
    query = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'ConnectUs'