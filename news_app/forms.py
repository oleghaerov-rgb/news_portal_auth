from django import forms

class NewsForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label='Заголовок'
    )

    summary = forms.CharField(
        max_length=200,
        label='Краткое описание'
    )

    content = forms.CharField(
        widget=forms.Textarea,
        label='Текст новости'
    )