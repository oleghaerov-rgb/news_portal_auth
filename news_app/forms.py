from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import News


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=150, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=150, required=True)
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
        labels = {
            'username': 'Логин',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username__iexact=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Этот логин уже занят.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'title',
            'summary',
            'content',
        ]
        labels = {
            'title': 'Заголовок',
            'summary': 'Краткое описание',
            'content': 'Текст новости',
        }
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 5:
            raise forms.ValidationError('Заголовок должен быть не короче 5 символов.')
        return title

    def clean_summary(self):
        summary = self.cleaned_data['summary'].strip()
        if len(summary) < 10:
            raise forms.ValidationError('Описание должно быть не короче 10 символов.')
        return summary

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if len(content) < 20:
            raise forms.ValidationError('Текст новости должен быть не короче 20 символов.')
        return content
