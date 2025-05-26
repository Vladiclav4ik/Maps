from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from .forms import MapImageForm, MapEditForm
from .models import MapImage
from django.shortcuts import render, redirect
from django.urls import reverse

@login_required
def map_view(request):
    user = User.objects.get(username=request.user.username)
    maps = MapImage.objects.filter(author=user)
    referer = request.META.get('HTTP_REFERER', reverse('map_view'))
    return render(request, 'map_view.html', {'maps': maps, 'back_url': referer})

@login_required
def all_maps(request):
    maps = MapImage.objects.filter(visibility="public")
    referer = request.META.get('HTTP_REFERER', reverse('map_view'))
    return render(request, 'all_map_view.html', {'maps': maps, 'back_url': referer})

@login_required
def upload_map(request):
    referer = request.META.get('HTTP_REFERER', reverse('map_view'))
    if request.method == 'POST':
        form = MapImageForm(request.POST, request.FILES)
        if form.is_valid():
            map_image = form.save(commit=False)
            map_image.nw_lat = request.POST.get('nw_lat')
            map_image.nw_lng = request.POST.get('nw_lng')
            map_image.ne_lat = request.POST.get('ne_lat')
            map_image.ne_lng = request.POST.get('ne_lng')
            map_image.sw_lat = request.POST.get('sw_lat')
            map_image.sw_lng = request.POST.get('sw_lng')
            map_image.author = request.user
            map_image.save()
            return redirect('main')
    else:
        form = MapImageForm()
    return render(request, 'upload_map.html', {
        'form': form,
        'back_url': referer
    })

@login_required
def map_detail(request, map_id):
    map_obj = get_object_or_404(MapImage, pk=map_id)
    user = map_obj.author
    public_name = user.profile.public_name

    referer = request.META.get('HTTP_REFERER')
    edit_url = reverse('edit_map', args=[map_id])

    # Сохраняем ссылку в сессию, если пользователь пришёл не с edit_map
    if referer:
        referer_path = urlparse(referer).path
        if referer_path != edit_url:
            request.session['from_before_edit'] = referer

    # back_url для кнопки "назад"
    back_url = request.session.get('from_before_edit', reverse('map_view'))

    return render(request, 'map_detail.html', {
        'map': map_obj,
        'back_url': back_url,
        'public_name': public_name,
    })

@login_required
def main(request):
    referer = request.META.get('HTTP_REFERER', reverse('main'))
    public_name = request.user.profile.public_name
    return render(request, 'main.html', {'back_url': referer, 'public_name': public_name})

@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    public_name = user.profile.public_name
    maps = MapImage.objects.filter(author=user, visibility="public")
    referer = request.META.get('HTTP_REFERER', reverse('map_view'))
    context = {
        'profile_user': user,
        'maps': maps,
        'back_url': referer,
        'public_name': public_name,
    }
    return render(request, 'profile.html', context)

@login_required
def delete_map(request, map_id):
    map_obj = get_object_or_404(MapImage, pk=map_id)

    # Проверяем, что пользователь — автор карты
    if map_obj.author != request.user:
        return redirect('main')  # Или выбросить 403

    if request.method == 'POST':
        map_obj.delete()
        return redirect('main')  # Перенаправление после удаления

    # При GET запросе показываем подтверждение удаления
    return render(request, 'confirm_delete.html', {'map': map_obj})

@login_required
def edit_map(request, map_id):
    map_obj = get_object_or_404(MapImage, pk=map_id)

    # Проверка, что пользователь — автор карты
    if map_obj.author != request.user:
        return redirect('main')  # Или 403 Forbidden

    if request.method == 'POST':
        form = MapEditForm(request.POST, request.FILES, instance=map_obj)
        if form.is_valid():
            edited_map = form.save(commit=False)
            # Если у карты есть координаты, обновляем их из POST, если они там есть
            edited_map.nw_lat = request.POST.get('nw_lat', edited_map.nw_lat)
            edited_map.nw_lng = request.POST.get('nw_lng', edited_map.nw_lng)
            edited_map.ne_lat = request.POST.get('ne_lat', edited_map.ne_lat)
            edited_map.ne_lng = request.POST.get('ne_lng', edited_map.ne_lng)
            edited_map.sw_lat = request.POST.get('sw_lat', edited_map.sw_lat)
            edited_map.sw_lng = request.POST.get('sw_lng', edited_map.sw_lng)

            edited_map.save()
            return redirect('map_detail', map_id=edited_map.id)
    else:
        form = MapEditForm(instance=map_obj)

    return render(request, 'edit_map.html', {'form': form, 'map': map_obj})


def redirect_to_login(request):
    return redirect('/login')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/maps')
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

def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()  # ✅ Вызовет form.save() с созданием Profile
            authenticated_user = authenticate(
                username=new_user.username,
                password=user_form.cleaned_data['password']
            )
            login(request, authenticated_user)
            return redirect('/main')  # ✅ На страницу профиля или главное меню
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})