# Generated by Django 4.2.10 on 2024-03-12 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appnews', '0005_alter_category_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categoryType',
            field=models.CharField(choices=[('NW', 'Новость'), ('AR', 'Статья')], default='AR', max_length=2, verbose_name='Тип: Статья/Новость:'),
        ),
        migrations.AlterField(
            model_name='post',
            name='dateCreation',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
