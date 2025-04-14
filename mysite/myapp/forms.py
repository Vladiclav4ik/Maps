from django import forms
from django.contrib.auth.models import User
from .models import Training
from .models import MapImage
import gpxpy
from datetime import timedelta


class TrainingForm(forms.ModelForm):
    distance = forms.DecimalField(label='Distance (km)', required=False)
    hours = forms.IntegerField(label='hours', required=False)
    minutes = forms.IntegerField(label='minutes', required=False)
    seconds = forms.IntegerField(label='seconds', required=False)
    route = forms.FileField(label='File gpx', required=False)

    class Meta:
        model = Training
        fields = ['name','activity_type', 'route', 'distance', 'hours', 'minutes', 'seconds', 'rating', ]

    def clean(self):
        cleaned_data = super().clean()
        route_file = cleaned_data.get('route')
        distance = cleaned_data.get('distance')
        hours = cleaned_data.get('hours')
        minutes = cleaned_data.get('minutes')
        seconds = cleaned_data.get('seconds')

        if not route_file and (distance is None or ( hours is None and minutes is None and seconds is None)):
            raise forms.ValidationError("Either upload a route file or enter distance and time manually.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        route_file = self.cleaned_data.get('route')
        manual_distance = self.cleaned_data.get('distance')
        hours = self.cleaned_data.get('hours')
        minutes = self.cleaned_data.get('minutes')
        seconds = self.cleaned_data.get('seconds')
        if route_file:
            gpx_data = route_file.read()
            gpx = gpxpy.parse(gpx_data)
            distance = sum(track.length_3d() for track in gpx.tracks) / 1000  # Преобразуем в километры
            time_seconds = sum(track.get_duration() for track in gpx.tracks)
            time = timedelta(seconds=time_seconds)
        else:
            distance = manual_distance
            time = timedelta(hours=hours, minutes=minutes, seconds=seconds)

        instance.distance = distance
        instance.time = time


        if commit:
            instance.save()
        return instance


class LoginForm (forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

from django import forms
from .models import MapImage

class MapImageForm(forms.ModelForm):
    class Meta:
        model = MapImage
        fields = ['title','property','image']

