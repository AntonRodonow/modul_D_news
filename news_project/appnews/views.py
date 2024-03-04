from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

# Create your views here.
# from django.core.paginator import Paginator  # Для будущей пагинации после фитьрации кверисета статей
# from django.shortcuts import render  # # Для будущей пагинации после фитьрации кверисета статей
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category
from datetime import datetime


class PostList(ListView):
    """
    Вывод новостей и статей, либо только статей, либо только новостей
    """
    model = Post
    template_name = 'appnews/posts.html'  # почему не работает автоматическое определение положения шаблона в папке темплейтс???
    context_object_name = 'posts'  # вызов объекта из шаблона
    ordering = '-id'  # или queryset = Post.objects.order_by('-id')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        context['time_now'] = datetime.utcnow()
        context['news'] = Post.objects.all()
        context['Article'] = Post.objects.filter(categoryType="AR")
        context['New'] = Post.objects.filter(categoryType="NW")
        return context


class PostDetailView(DetailView):
    """
    Детали новости или статьи
    """
    queryset = Post.objects.all()
    template_name = 'appnews/post_detail.html'
    context_object_name = 'post'


class PostAddView(PermissionRequiredMixin, CreateView):
    """
    Добавить статью или новость
    """
    form_class = PostForm
    model = Post
    template_name = 'appnews/post_add.html'
    permission_required = ('appnews.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/appnews/news/create/':
            post.categoryType = 'NW'
        post.save()
        return super().form_valid(form)


class PostListFilter(ListView):
    """ Поиск новости по автору и датам.
    Пагинация в фитрованном кверисете не реализована,
    нужно перепоределение в контексте page_obj и is_paginated.
    Временно оставил нерабочую пагинацию в шаблоне до решения проблемы"""
    model = Post
    template_name = 'appnews/postsfilter.html'
    ordering = '-id'
    paginate_by = 1  # пагинация не в фильтре не раелизована, нужно пероепредеять контекст для шаблона
    # paginator = Paginator(objects, 1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        # context['page_obj'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    # def list_f(self, request):
    #     list_filtered = PostFilter(self.request.GET, queryset=self.get_queryset())
    #     paginator = Paginator(list_filtered, 1)
    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)
    #     return render(request, "postsfilter.html", {"page_obj": page_obj})


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Редактирование статьи или новости
    """
    form_class = PostForm
    template_name = 'appnews/post_add.html'
    permission_required = ('appnews.change_post',)

    def get_object(self, **kwargs):  # без него не видит кверисет
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление статей или новостей
    """
    queryset = Post.objects.all()
    template_name = 'appnews/post_delete.html'
    success_url = '/appnews'


# class CategoryView(FormView, View, Category):  # добавил View, Category, Post вероятно не нужны!!!!! (старый комент, проверю)
#     # form_class = CategorySubscribers
#     template_name = 'appnews/subscribers.html'
#     success_url = '/appnews'
