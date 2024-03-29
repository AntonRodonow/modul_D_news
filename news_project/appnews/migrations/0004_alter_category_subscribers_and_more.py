# Generated by Django 4.2.10 on 2024-03-09 13:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appnews', '0003_alter_post_categorytype_delete_categoryview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='categories', to=settings.AUTH_USER_MODEL, verbose_name='Подписчики:'),
        ),
        migrations.AlterField(
            model_name='post',
            name='postArticleCategory',
            field=models.ManyToManyField(related_name='post', through='appnews.PostCategory', to='appnews.category'),
        ),
    ]
