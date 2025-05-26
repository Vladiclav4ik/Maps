from django import forms
from django.contrib.auth.models import User
from .models import MapImage, Profile

class LoginForm (forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    public_name = forms.CharField(
        label='Публичное имя',
        max_length=150,
        help_text='Имя, которое будет видно другим пользователям.'
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                public_name=self.cleaned_data['public_name']
            )
        return user

from django import forms
from .models import MapImage

class MapImageForm(forms.ModelForm):
    title = forms.CharField(
        label='Название',
        widget=forms.TextInput(attrs={
            'class': 'custom-input',
            'placeholder': 'Введите название карты',
            'autocomplete': 'off',
        })
    )

    description = forms.CharField(
        label='Описание',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'custom-textarea',
            'placeholder': 'Введите описание карты',
            'rows': 4,
            'style': 'resize: vertical;',
        })
    )

    visibility = forms.ChoiceField(
        label='Приватность',
        choices=[
            ('public', 'Публичная'),
            ('private', 'Приватная'),
        ],
        widget=forms.Select(attrs={
            'class': 'custom-select',
        })
    )

    image = forms.ImageField(
        label='Выберите файл',
        widget=forms.ClearableFileInput(attrs={
            'class': 'custom-file-input',
        })
    )

    class Meta:
        model = MapImage
        fields = ['title', 'description', 'visibility', 'image']


class MapEditForm(forms.ModelForm):
    title = forms.CharField(
        label='Название',
        widget=forms.TextInput(attrs={
            'class': 'custom-input',
            'placeholder': 'Введите название карты',
            'autocomplete': 'off',
        })
    )

    description = forms.CharField(
        label='Описание',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'custom-textarea',
            'placeholder': 'Введите описание карты',
            'rows': 4,
            'style': 'resize: vertical;',
        })
    )

    visibility = forms.ChoiceField(
        label='Приватность',
        choices=[
            ('public', 'Публичная'),
            ('private', 'Приватная'),
        ],
        widget=forms.Select(attrs={
            'class': 'custom-select',
        })
    )

    class Meta:
        model = MapImage
        fields = ['title', 'description', 'visibility']

