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

from django.db import models
from django.contrib.auth.models import User

class MapImage(models.Model):
    PROPERTY_CHOICES = [
        ('private', 'Личное'),
        ('public', 'Общее'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.CharField(
        max_length=10,
        choices=PROPERTY_CHOICES,
        default='private'
    )
    title = models.CharField(max_length=255, default='Untitled')
    image = models.ImageField(upload_to='maps/')
    nw_lat = models.FloatField()  # Северо-западная широта
    nw_lng = models.FloatField()  # Северо-западная долгота
    ne_lat = models.FloatField()  # Северо-восточная широта
    ne_lng = models.FloatField()  # Северо-восточная долгота
    sw_lat = models.FloatField()  # Юго-западная широта
    sw_lng = models.FloatField()  # Юго-западная долгота

    def __str__(self):
        return f"Image Map {self.id} - {self.image.url}"

    class Meta:
        verbose_name = "Image Map"
        verbose_name_plural = "Image Maps"
