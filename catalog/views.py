from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import BlogPost  # Правильный импорт модели


class BlogListView(ListView):
    """Список блоговых записей"""
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        """Выводим только опубликованные статьи"""
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


class BlogDetailView(DetailView):
    """Детальная страница блоговой записи"""
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Увеличиваем счетчик просмотров"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogCreateView(CreateView):
    """Создание блоговой записи"""
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def form_valid(self, form):
        """Добавление сообщения об успешном создании статьи"""
        messages.success(self.request, "Статья успешно создана!")
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправление на детальную страницу созданной статьи"""
        return reverse('blog:blog_detail', kwargs={'pk': self.object.pk})


class BlogUpdateView(UpdateView):
    """Редактирование блоговой записи"""
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def form_valid(self, form):
        """Добавление сообщения об успешном обновлении статьи"""
        messages.success(self.request, "Статья успешно обновлена!")
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправление на детальную страницу отредактированной статьи"""
        return reverse('blog:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    """Удаление блоговой записи"""
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')

    def delete(self, request, *args, **kwargs):
        """Добавление сообщения об успешном удалении статьи"""
        obj = self.get_object()
        messages.success(self.request, f"Статья '{obj.title}' успешно удалена!")
        return super().delete(request, *args, **kwargs)