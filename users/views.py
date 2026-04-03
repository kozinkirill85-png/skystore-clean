from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm
from .models import User



class RegisterView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Отправка приветственного письма"""
        response = super().form_valid(form)

        # Отправка приветственного письма
        send_mail(
            subject='Добро пожаловать в Skystore!',
            message=f'Здравствуйте, {self.object.email}!\n\n'
                    f'Спасибо за регистрацию в нашем интернет-магазине.\n'
                    f'Мы рады видеть вас в нашей команде!\n\n'
                    f'С наилучшими пожеланиями,\n'
                    f'Команда Skystore',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
            fail_silently=False,
        )

        return response


class LoginView(LoginView):
    """Авторизация пользователя"""
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')

    def get_success_url(self):
        """Перенаправление после успешного входа"""
        return reverse('catalog:home')


class LogoutView(LogoutView):
    """Выход из системы"""
    next_page = reverse_lazy('catalog:home')
