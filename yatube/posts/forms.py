from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст вашего поста здесь'}),
            'group': forms.Select(attrs={
                'class': 'form-control',
                'title': 'Выберите группу для публикации'}),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
                'title': 'Выберите изображение для поста'}),
        }
