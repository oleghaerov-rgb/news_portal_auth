from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import News
from .forms import NewsForm, RegisterForm, UserUpdateForm


def home_view(request):
    news_list = News.objects.all().order_by(
        '-date_created'
    )
    paginator = Paginator(news_list, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'home.html',
        {
            'page_obj': page_obj,
            'news_list': page_obj,
        }
    )


def news_detail_view(request, news_id):
    news = get_object_or_404(
        News,
        id=news_id
    )

    return render(
        request,
        'news_detail.html',
        {
            'news': news
        }
    )


@login_required
def news_create_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)

        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Новость успешно добавлена.')
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm()

    return render(
        request,
        'news_form.html',
        {
            'form': form,
            'page_title': 'Добавить новость',
            'button_text': 'Сохранить новость',
        }
    )


@login_required
def news_edit_view(request, news_id):
    news = get_object_or_404(News, id=news_id)

    if news.author != request.user:
        return HttpResponseForbidden('Вы не можете редактировать эту новость.')

    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно обновлена.')
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm(instance=news)

    return render(
        request,
        'news_form.html',
        {
            'form': form,
            'news': news,
            'page_title': 'Редактировать новость',
            'button_text': 'Сохранить изменения',
        }
    )


@login_required
def news_delete_view(request, news_id):
    news = get_object_or_404(News, id=news_id)

    if news.author != request.user:
        return HttpResponseForbidden('Вы не можете удалить эту новость.')

    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость удалена.')
        return redirect('home')

    return render(
        request,
        'news_confirm_delete.html',
        {
            'news': news,
        }
    )


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен.')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(
        request,
        'profile.html',
        {
            'form': form,
        }
    )


@login_required
def profile_delete_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Аккаунт удален.')
        return redirect('home')

    return render(
        request,
        'profile_confirm_delete.html'
    )
