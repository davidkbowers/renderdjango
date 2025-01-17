from django.db import models
from django.utils import timezone

# Create your models here.

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    eventdatetime = models.DateTimeField()
    address = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'event'
        ordering = ['eventdatetime']


class Register(models.Model):
    id = models.AutoField(primary_key=True)
    date_registered = models.DateTimeField()
    cancelled = models.BooleanField(default=False)
    email = models.EmailField()  # Changed from TextField to EmailField for better validation
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.event.title if self.event else 'No Event'}"

    class Meta:
        db_table = 'register'


class Subscriber(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    opted_out = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        db_table = 'subscriber'
        ordering = ['-created_at']
