from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    """
    Форма для создания статей
    """

    class Meta:
        model = Post
        fields = ['author',
                  'postArticleCategory',
                  'title',
                  'text',
                  'rating']
        labels = {
            'postArticleCategory': 'Категория'
        }

    def clean(self):
        """
        Валидация формы. Есть валидация и во вьюшке
        """
        cleand_form = super().clean()
        text = cleand_form.get('text')
        if text is not None and len(text) < 6:
            raise ValidationError({
                "text": "Текст статьи или новости не может быть менее 6 символов."
            })

        title = cleand_form.get('title')
        if title is not None and len(title) < 6 and title == text:
            raise ValidationError({
                "title": "Текст статьи или новости идентичен ее содержанию и быть короче 6 символов"
            })
        return cleand_form
