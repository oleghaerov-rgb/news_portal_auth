from datetime import date

from django.http import Http404
from django.shortcuts import render, redirect

from .forms import NewsForm
from .utils import load_news, save_news


def home_view(request):
    news_list = load_news()

    news_list = sorted(
        news_list,
        key=lambda x: x['date'],
        reverse=True
    )

    return render(
        request,
        'home.html',
        {
            'news_list': news_list,
            'today': str(date.today())
        }
    )


def news_detail_view(request, news_id):
    news_list = load_news()

    news = next(
        (n for n in news_list if n['id'] == news_id),
        None
    )

    if news is None:
        raise Http404("Новость не найдена")

    return render(
        request,
        'news_detail.html',
        {'news': news}
    )


def add_news_view(request):
    if request.method == 'POST':

        form = NewsForm(request.POST)

        if form.is_valid():

            news_list = load_news()

            new_id = max(
                (n['id'] for n in news_list),
                default=0
            ) + 1

            news_item = {
                'id': new_id,
                'title': form.cleaned_data['title'],
                'summary': form.cleaned_data['summary'],
                'content': form.cleaned_data['content'],
                'date': str(date.today())
            }

            news_list.append(news_item)

            save_news(news_list)

            return redirect('success')

    else:
        form = NewsForm()

    return render(
        request,
        'add_news.html',
        {'form': form}
    )


def success_view(request):
    return render(
        request,
        'success.html'
    )