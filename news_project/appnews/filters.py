from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter


from .models import Post


class PostFilter(FilterSet):
    """
    Фильтр по автору и датам
    """
    dateStart = DateTimeFilter(field_name='dateCreation', lookup_expr='gt', widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}),)
    dateFinish = DateTimeFilter(field_name='dateCreation', lookup_expr='lt', widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}),)

    class Meta:
        model = Post
        fields = ['author']
