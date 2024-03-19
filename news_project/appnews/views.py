from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
# from django.core.paginator import Paginator  # Для будущей пагинации после фитьрации кверисета статей
# from django.shortcuts import render  # # Для будущей пагинации после фитьрации кверисета статей
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # FormView

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category  # PostCategory
from datetime import datetime
from news_project.settings import SERVER_EMAIL


# if __package__ is None or __package__ == '':  # интересная конструкция, потом почитать побольше
#     from news_project.settings import SERVER_EMAIL
# else:
#     from news_project.settings import SERVER_EMAIL


class PostList(ListView):
    """
    Вывод новостей и статей, либо только статей, либо только новостей
    """
    model = Post
    template_name = 'appnews/posts.html'
    context_object_name = 'posts'  # вызов объекта из шаблона - поскольку есть поле model = Post, можно задать так, а можно, как сейчас, в get_context_data
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
    Опубликовать статью или новость
    """
    form_class = PostForm
    model = Post
    template_name = 'appnews/post_add.html'
    permission_required = ('appnews.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/appnews/news/create/':
            post.categoryType = 'NW'
        post.save
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

    # для пагинации:
    # def list_f(self, request):
    #     list_filtered = PostFilter(self.request.GET, queryset=self.get_queryset())
    #     paginator = Paginator(list_filtered, 1)
    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)
    #     return render(request, "postsfilter.html", {"page_obj": page_obj})


class PostUpdateView(PermissionRequiredMixin, UpdateView):  # убрал лишнее LoginRequiredMixin,
    """
    Редактирование статьи или новости
    """
    form_class = PostForm
    template_name = 'appnews/post_add.html'
    permission_required = ('appnews.change_post',)

    def get_object(self, **kwargs):  # без него не видит кверисет
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Удаление статей или новостей
    """
    queryset = Post.objects.all()
    template_name = 'appnews/post_delete.html'
    success_url = '/appnews'
    permission_required = ('appnews.delete_post',)


class CategoryListView(ListView):
    """
    Отображение публикаций одной выбранной категории
    """
    model = Post
    template_name = 'appnews/category_list.html'
    context_object_name = 'category_news_list'  # список постов в одной категории

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])  # здесь хранится одна конкретная категория
        queryset = Post.objects.filter(postArticleCategory=self.category).order_by('-dateCreation')  # сортировка по дате создания статьи, аналогично -id
        return queryset  # переопределили поле category и добавили его в контекст ниже

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_subscriber'] = self.request.user in self.category.subscribers.all()  # True если юзер не подписан на категорию
        context['category'] = self.category  # ссылка через модель Post на модель Category (меняю postArticleCategory тут и выше строкой)
        context['posts'] = Post.objects.all()  # Возможно работет без этой строки, подхватывая из модели Post, т.к. мы загружаем модель Post в первой строкой вьюшки
        context['catpost'] = Post.objects.filter(postArticleCategory=self.category)  # Возможно работет без этой строки, подхватывая из модели Post, т.к. мы загружаем модель Post в первой строкой вьюшки
        context['categorylistview'] = True  # проверка для теплейтса, не обязательная, но пусть останется для примера
        return context


@login_required   # еще один способ на заметку
def subscribe(request, pk):
    """Добавление подписки для user на категории публикаций (класса Category).
    Отправка письма о новой подписке user"""
    user = request.user
    uid = user.id
    category = Category.objects.get(id=pk)
    qSub = category.subscribers.all()
    print(qSub, 'Подписчики:', category)

    if not qSub.filter(username=user).exists():  # в данном случае сообщение заменено на html файл
        category.subscribers.add(user)
        message = f'{request.user}, вы подписались на рассылку публикаций категории: "{category}".'
    else:
        category.subscribers.remove(user)
        message = f'Пользователь {user} отписался от категории публикаций: "{category}".'

    try:
        email = category.subscribers.get(id=uid).email
        # print(f'email: "{email}" Можно отправить уведомление')
        send_mail(
            subject=f'News Portal: подписка на обновления категории {category}',
            message=f'«{user}», вы подписались на обновление категории: «{category}».',
            from_email=SERVER_EMAIL,
            recipient_list=[f'{email}', ],
        )

    except Exception as e:
        print('Exception вызван для попытки отправить письмо подписчикам о успешной подписке')
    return render(request, 'appnews/subscribe.html', {'category': category,
                                                      'message': message, 'user': user.username})
    # словарь последним аргументом это замена контекста для шаблона (доступно для render())
