from django.contrib.auth.views import LoginView
from django.urls import path

from .views import PostList, PostDetailView, PostAddView, PostUpdateView, PostDeleteView, PostListFilter, \
    CategoryListView, subscribe  # CategoryView,


urlpatterns = [
    path('', PostList.as_view()),  # Вывод всех статей и новостей на главной странице. Нужено!
    path('Articles/', PostList.as_view()),  # Вывод только статей. Нужено!
    path('News/', PostList.as_view()),  # Вывод только новостей. Нужено!
    path('<int:pk>/', PostDetailView.as_view(), name='news_detail'),  # урл, представление, ссылка в шаблоне. Датали новости/статьи. Нужно!
    path('news/create/', PostAddView.as_view(), name='news_add'),  # Добавить новость. Нужно!
    path('articles/create/', PostAddView.as_view(), name='articles_add'),  # Добавить статью. Нужно!
    path('search/', PostListFilter.as_view()),  # поиск новости/статьи по автору и датам. Нужно!
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='news_update'),  # редактирование новости. Нужно!
    path('articles/<int:pk>/edit/', PostUpdateView.as_view(), name='articles_update'),  # редактирование статьи. Реализовано только для страницы вывода только статей. Нужно!
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),  # удлать новость. Нужно!
    path('articles/<int:pk>/delete/', PostDeleteView.as_view(), name='articles_delete'),  # удлать статью. Нужно!
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribers/', subscribe, name='subscribe'),

    # path('subscribers/', CategoryView.as_view(template_name='newapp/subscribers.html'), name='subscribers'),  # старая реализация через форму
    # path('index/', index)  #test celery
    ]
