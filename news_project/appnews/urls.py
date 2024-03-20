from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostList, PostDetailView, PostAddView, PostUpdateView, PostDeleteView, PostListFilter, \
    CategoryListView, subscribe  # CategoryView,


urlpatterns = [
    path('', cache_page(60)(PostList.as_view())),  # Вывод всех статей и новостей на главной странице. Нужено!
    path('Articles/', PostList.as_view()),  # Вывод только статей. Нужено!
    path('News/', PostList.as_view()),  # Вывод только новостей. Нужено!
    path('<int:pk>/', cache_page(60*2)(PostDetailView.as_view()), name='news_detail'),  # Урл, представление, ссылка в шаблоне. Датали новости/статьи. Нужно!
    path('news/create/', PostAddView.as_view(), name='news_add'),  # Добавить новость. Нужно!
    path('articles/create/', PostAddView.as_view(), name='articles_add'),  # Добавить статью. Нужно!
    path('search/', PostListFilter.as_view()),  # Поиск новости/статьи по автору и датам. Нужно!
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='news_update'),  # Редактирование новости. Нужно!
    path('articles/<int:pk>/edit/', PostUpdateView.as_view(), name='articles_update'),  # Редактирование статьи. Реализовано только для страницы вывода только статей. Нужно!
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),  # Удлать новость. Нужно!
    path('articles/<int:pk>/delete/', PostDeleteView.as_view(), name='articles_delete'),  # Удлать статью. Нужно!
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribers/', subscribe, name='subscribe'),

    # path('index/', index)  #test celery
    ]
