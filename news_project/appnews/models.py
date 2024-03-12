from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор:')  # db_index=True попробовать позже
    ratingAuthor = models.SmallIntegerField(default=0, verbose_name="Рейтинг:")

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')
        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser.username}'

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Category(models.Model):
    """ 4 категории публикаций"""
    name = models.CharField(max_length=64, unique=True, verbose_name="Категория:")
    subscribers = models.ManyToManyField(User, blank=True, verbose_name="Подписчики/пользователи:",  # в админ панели мени ту мени не отображаются, нельзя просто добавлять и убирать подписчиков
                                         related_name='categories')  # related_name для не использования _set, нужной для обратной связей

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    author = models.ForeignKey(to="Author", on_delete=models.CASCADE, verbose_name='Автор:')

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE,
                                    verbose_name="Тип: Статья/Новость:")
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, verbose_name="Заголовок:")
    text = models.TextField(verbose_name="Текст поста:")
    rating = models.SmallIntegerField(default=0, verbose_name="Рейтинг:")
    postArticleCategory = models.ManyToManyField(to="Category", through='PostCategory', related_name='post')  # verbose_name="Категория: .Сдалал для теста в forms.py

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]} ... с текущим рейтингом {str(self.rating)}'
        # return '{} ... {}'.format(self.text[0:123], str(self.rating))

    def get_absolute_url(self):
        # return f'http://127.0.0.1:8000/appnews/{self.id}'  # при добавлении новости переходит по этой ссылке
        return reverse('news_detail', args=[str(self.id)])  # альтернативнй вариант ссылки

    def get_category(self):
        return f'{self.postArticleCategory}'

    def message_subscriber(self):
        return f'Новая статья - "{self.title}" в разделе "{self.postArticleCategory.first()}".'

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Статья/Новость"
        verbose_name_plural = "Статьи/Новости"


class PostCategory(models.Model):
    """Такую отдельну табл. обычно не создают если не нужны
    дополнительные поля кроме ключей двух таблиц.
    Создана в учебных целях. Пример верного оформления в
    классе Category, поле subscribers"""
    postThrough = models.ForeignKey(to="Post", on_delete=models.CASCADE, verbose_name='Пост/Новость:')
    categoryThrough = models.ForeignKey(to="Category", on_delete=models.CASCADE, verbose_name='Категория:')

    def __str__(self):
        return f'{self.postThrough}\t...\t{self.categoryThrough}'  # найти способ ставить табуляцию в админ панели

    class Meta:
        verbose_name = "Пост-Категория"
        verbose_name_plural = "Посты-Категории"


class Comment(models.Model):
    commentPost = models.ForeignKey(to="Post",
                                    on_delete=models.CASCADE, verbose_name='На пост:')  # related_name='comment',
    # если надо ссылать в шаблоне через коммент на пост, т.к. с комента на пост нет прямой ссылки, только связь по
    # ключу, а значит и вызов тольк очерез .commentPost_set, работает со всеми полями models
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='На автора:')
    text = models.TextField(editable=True, help_text='Тут хелп текст к коментариям', verbose_name="Коментарий:")
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания:")
    rating = models.SmallIntegerField(default=0, verbose_name="Рейтинг:")

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"


# class Subscription(models.Model):
#     """Таблица Юзера к категориям. ManyToMany"""
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Пользователь:')
#     category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Категории:')
