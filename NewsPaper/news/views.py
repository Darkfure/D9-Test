from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, article, news, Category, PostCategory
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def notify_managers_appointment(sender, instance, action, **kwargs):
    if action == 'post_add':
        print(instance)
        sub_users = Category.objects.filter(id=instance.category).values('subscribers__email')
        print(sub_users)
        # sub_males = []
        #
        # for i in range(len(sub_users)):
        #     sub_males.append(sub_users[i]['subscribers__email'])
        sub_males = [sub['subscribers__email'] for sub in sub_users]

        send_mail(
            subject=f'{instance.category.name}: {instance.heading}',
            # имя клиента и дата записи будут в теме для удобства
            message=instance.text,  # сообщение с кратким описанием проблемы
            from_email='lion4652@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=sub_males  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )

        # html_content = render_to_string(
        #     'post_for_send.html',
        #     {
        #         'post': instance,
        #     }
        # )
        #
        # msg = EmailMultiAlternatives(
        #     subject=f'{instance.category.name}: {instance.heading}',
        #     body=instance.text,  # это то же, что и message
        #     from_email='lion4652@yandex.ru',
        #     to=sub_males,  # это то же, что и recipients_list
        # )
        # msg.attach_alternative(html_content, "text/html")  # добавляем html
        #
        # msg.send()
    # action = 'post_add'
    # sub_users = Category.objects.filter(id=instance.category).values('subscribers__email')
    # sub_males = []
    #
    # for i in range(len(sub_users)):
    #     sub_males.append(sub_users[i]['subscribers__email'])

    # if created:
    #     subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    # else:
    #     subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'
    #
    # mail_managers(
    #     subject=subject,
    #     message=instance.message,
    # )
        # получаем наш html
    # html_content = render_to_string(
    #     'post_for_send.html',
    #     {
    #         'post': instance,
    #     }
    # )
    # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же. (возможно выбрать фильтром юзеров почта = user.email)
    # msg = EmailMultiAlternatives(
    #     subject=f'{instance.category.name}: {instance.heading}',
    #     body=instance.text,  # это то же, что и message
    #     from_email='lion4652@yandex.ru',
    #     to=sub_males,  # это то же, что и recipients_list
    # )
    # msg.attach_alternative(html_content, "text/html")  # добавляем html
    #
    # msg.send()  # отсылаем

    # return redirect('appointments:make_appointment')


class PostsList(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'articles' in self.request.path:
            post.type = article
        else:
            post.type = news
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     post = Post(
    #         heading=request.POST['heading'],
    #         text=request.POST['text'],
    #     )
    #     post.save()
    #
    #     # получаем наш html
    #     html_content = render_to_string(
    #         'post_for_send.html',
    #         {
    #             'post': post,
    #         }
    #     )
    #
    #     # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же. (возможно выбрать фильтром юзеров почта = user.email)
    #     msg = EmailMultiAlternatives(
    #         subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
    #         body=appointment.message,  # это то же, что и message
    #         from_email='peterbadson@yandex.ru',
    #         to=['skavik46111@gmail.com'],  # это то же, что и recipients_list
    #     )
    #     msg.attach_alternative(html_content, "text/html")  # добавляем html
    #
    #     msg.send()  # отсылаем
    #
    #     return redirect('appointments:make_appointment')


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class Categories(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    chosen_cat = Category.objects.get(id=pk)

    if not chosen_cat.subscribers.filter(id=user.id).exists():
        chosen_cat.subscribers.add(user)

    return redirect('/')

# @login_required
# def unsubscribe_from_category(request, pk):
#     user = request.user
#     chosen_cat = Category.objects.get(id=pk)
#
#     if not chosen_cat.subscribers.filter(id=user.id).exists():
#         chosen_cat.subscribers.add(user)
#
#     return redirect('/')
