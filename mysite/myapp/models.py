from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Training(models.Model):
    ACTIVITY_CHOICES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    name = models.CharField(max_length=40, default='Training')
    route = models.FileField(upload_to='gpx/')
    distance = models.DecimalField(max_digits=6, decimal_places=2)  # Километраж
    time = models.DurationField()  # Время
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])  # Оценка состояния
