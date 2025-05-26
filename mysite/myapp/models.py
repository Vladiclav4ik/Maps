from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    public_name = models.CharField(
        max_length=150,
        default= 'Me',
        verbose_name="Публичное имя",
        help_text="Имя, отображаемое другим пользователям"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class MapImage(models.Model):
    PROPERTY_CHOICES = [
        ('private', 'Личная'),
        ('public', 'Публичная'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    visibility = models.CharField(
        max_length=10,
        choices=PROPERTY_CHOICES,
        default='private',
        verbose_name="Приватность"
    )
    title = models.CharField(max_length=255, default='Без названия', verbose_name="Название карты")
    description = models.TextField( blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='maps/', verbose_name="Файл карты")
    nw_lat = models.FloatField()  # Северо-западная широта
    nw_lng = models.FloatField()  # Северо-западная долгота
    ne_lat = models.FloatField()  # Северо-восточная широта
    ne_lng = models.FloatField()  # Северо-восточная долгота
    sw_lat = models.FloatField()  # Юго-западная широта
    sw_lng = models.FloatField()  # Юго-западная долгота

    def __str__(self):
        return f"Image Map {self.id} - {self.image.url}"

    @property
    def center_lat(self):
        return (self.nw_lat + self.sw_lat) / 2

    @property
    def center_lng(self):
        return (self.nw_lng + self.ne_lng) / 2

    class Meta:
        verbose_name = "Image Map"
        verbose_name_plural = "Image Maps"
