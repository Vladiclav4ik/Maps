from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import LoginForm
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from .models import Training
from .forms import TrainingForm
from datetime import timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
@login_required
def training_detail(request, pk):
    training = get_object_or_404(Training, pk=pk)
    return render(request, 'training_detail.html', {'training': training})

@login_required
def maps(request):
    
    return render(request, 'training_detail.html', {'training': training})

@login_required
def add_training(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES)
        if form.is_valid():
            training = form.save(commit=False)
            training.author = request.user
            training.save()
            return redirect('training_list')  # Перенаправляем на страницу со списком тренировок
    else:
        form = TrainingForm()
    return render(request, 'add_training.html', {'form': form})


@login_required
def training_list(request):
    trainings = Training.objects.all()
    return render(request, 'training_list.html', {'trainings': trainings})

def redirect_to_login(request):
    return redirect('/login')
@login_required
def main(request):
    user = User.objects.get(username=request.user.username)
    trainings = Training.objects.filter(author=user)
    total_distance = 0
    total_time = timedelta()
    total_rating = 0
    num_trainings = 0

    for training in trainings:
        total_distance += training.distance
        total_time += training.time
        total_rating += training.rating
        num_trainings += 1

    if num_trainings > 0:
        average_distance = total_distance
        average_time = total_time
        average_rating = round(total_rating / num_trainings, 2)
    else:
        average_distance = 0
        average_time = 0
        average_rating = 0
    trainings = trainings[:1]
    return render(request, 'main.html', {'user': user, 'trainings': trainings,
                                            'avg_dist': average_distance, 'avg_time': average_time,
                                            'avg_rating': average_rating})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/main')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/main')
                else:
                    form.add_error(None, 'Disabled acc')
            else:
                form.add_error(None, 'Invalid login')
    else:
        form = LoginForm()
    return render(request, 'Registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)  # Разлогиниваем пользователя
    return redirect('/login')

def mysite (request):
    return render (request, 'O-TR.html')
def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            authenticated_user = authenticate(username=new_user.username, password=user_form.cleaned_data['password'])
            login(request, authenticated_user)

            return redirect('/main')  # Перенаправление на страницу профиля
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

@login_required
def view_profile(request, username):
    user = User.objects.get(username=username)
    trainings = Training.objects.filter(author=user)
    total_distance = 0
    total_time = timedelta()
    total_rating = 0
    num_trainings = 0

    for training in trainings:
        total_distance += training.distance
        total_time += training.time
        total_rating += training.rating
        num_trainings += 1

    if num_trainings > 0:
        average_distance = total_distance
        average_time = total_time
        average_rating = round(total_rating / num_trainings, 2)
    else:
        average_distance = 0
        average_time = 0
        average_rating = 0
    trainings = trainings[:3]
    return render(request, 'profile.html', {'user': user, 'trainings': trainings,
                                            'avg_dist': average_distance, 'avg_time': average_time,
                                            'avg_rating': average_rating})


def generate_pdf(request, training_id):
    training = get_object_or_404(Training, id=training_id)

    # Создание HttpResponse объекта с соответствующим заголовком
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="training_{training_id}.pdf"'

    # Создание буфера BytesIO для PDF
    buffer = BytesIO()

    # Создание canvas объекта с помощью reportlab
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Заполнение PDF содержимым
    p.drawString(100, height - 100, f'Training ID: {training.id}')
    p.drawString(100, height - 120, f'Author: {training.author.username}')
    p.drawString(100, height - 140, f'Activity Type: {training.get_activity_type_display()}')
    p.drawString(100, height - 160, f'Name: {training.name}')
    p.drawString(100, height - 180, f'Distance: {training.distance} km')
    p.drawString(100, height - 200, f'Time: {training.time}')
    p.drawString(100, height - 220, f'Rating: {training.rating}')

    # Завершение страницы
    p.showPage()
    p.save()

    # Перемотка буфера до начала
    buffer.seek(0)

    # Возвращение созданного PDF в HttpResponse
    response.write(buffer.getvalue())
    return response