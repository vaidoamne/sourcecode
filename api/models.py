from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train_number = models.CharField(max_length=50)
    departure = models.CharField(max_length=100)
    arrival = models.CharField(max_length=100)
    date = models.DateField()
    selected_seats = models.JSONField(default=list)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookings'

class SupportTicket(models.Model):
    PRIORITY_CHOICES = (
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    )
    CATEGORY_CHOICES = (
        ('booking', 'Booking'),
        ('technical', 'Technical'),
        ('payment', 'Payment'),
        ('other', 'Other')
    )

    user_id = models.CharField(max_length=100)  
    subject = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'support'

class Statistics(models.Model):
    active_trains = models.IntegerField(default=0)
    daily_passengers = models.IntegerField(default=0)
    revenue_today = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fuel_usage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    passenger_satisfaction = models.IntegerField(default=0)
    satisfaction_trend = models.JSONField(default=list)
    passenger_traffic = models.JSONField(default=list)
    train_status = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'statistics'
