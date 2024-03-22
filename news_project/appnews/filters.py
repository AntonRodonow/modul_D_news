from django.forms import DateTimeInput

from django_filters import DateTimeFilter, FilterSet

from .models import Post


class PostFilter(FilterSet):
    """Фильтрация новостей/постов по автору и датам."""

    date_start = DateTimeFilter(field_name='dateCreation', lookup_expr='gt', widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),)
    date_finish = DateTimeFilter(field_name='dateCreation', lookup_expr='lt', widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),)

    class Meta:
        model = Post
        fields = ['author']
