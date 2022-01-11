from django.db import models

# Create your models here.


class MailReport(models.Model):
    recipients = models.TextField()
    sender = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=200)
    # status = models.TextChoices()

    def __str__(self) -> str:
        return (str(self.timestamp)+self.subject)
