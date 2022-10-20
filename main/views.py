from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
# Примесь LoginRequiredMixin дает доступ только пользователю, выполнившему вход
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
# SuccessMessageMixin вывод всплывающих сообщений
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.signing import BadSignature
from django.core.paginator import Paginator
from django.db.models import Q


from .models import AdvUser, SubRubric, Bb
from .forms import ChangeUserInfoForm, RegisterUserForm, SearchForm
# signer вызывается для экономии оперативной памяти
from .utilities import signer

# Главная страница
def index(request):
    # вывод последних 10 объявлений
    bbs = Bb.objects.filter(is_active=True)[:10]
    context = {'bbs':bbs}
    return render(request, 'main/index.html', context)

# В качестве идентификатора страницы берет имя шаблона без пути и расширения
def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    # Если страница не существует, поднимает ошибку 404
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

# Страница входа
class BBLoginView(LoginView):
    template_name = 'main/login.html'

# Страница выхода
class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'

# Доступ к странице профиля возможен только после регистрации и при выполнении входа
@login_required
def profile(request):
    bbs = Bb.objects.filter(author=request.user.pk)
    context = {'bbs':bbs}
    return render(request, 'main/profile.html', context)

# Контроллер страницы основных данных с возможностью правки записи модели (текущего пользователя)
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = "Данные пользователя изменены"

    # переопределение метода setup для получения ключа текущего пользователя
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    # извлечение исправляемой записи
    def get_object(self, queryset=None):
        # получение набора записей методом get_queryset(), если таковой набор не был передан в параметре queryset
        if not queryset:
            queryset = self.get_queryset()
        # поиск записи, представлющую текущего пользователя
        return get_object_or_404(queryset, pk=self.user_id)

# Правка пароля
class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'

# Регистрация пользователя
class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')

# Сообщение о успешной регистрации
class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'

# Активация пользователя
def user_activate(request, sign):
    # Проверка цифровой подписи
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature/html')
    # Извлечение и поиск пользователя
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        # Непосредственно сама активация пользователя
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    
# Вывод объявлений из выбраной рубрики
def by_rubric(request, pk):
    # Извлечение выбраной рубрики
    rubric = get_object_or_404(SubRubric, pk=pk)
    # Выбор объявлений, относящихся к этой рубрике и помеченых для вывода (is_active)
    bbs = Bb.objects.filter(is_active=True, rubric=pk)
    # Фильтрация уже отобранных объявлений по введенному слову, взятому из GET-параметра keyword
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        # формирование на основе полученного слова объект фильтрации Q ( __icontains не чувствителен к регистру)
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    # создает экз. класса SearchForm, чтобы вывести его на экран. Передаем искомое слово, чтобы оно было в
    # выводимой на экран форме
    form = SearchForm(initial={'keyword':keyword})
    # пагинатор в параметре получает кол-во объявлений на странице
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric':rubric, 'page':page, 'bbs':page.object_list, 'form':form}
    return render(request, 'main/by_rubric.html', context)


def detail(request, rubric_pk, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {'bb':bb, 'ais':ais}
    return render(request, 'main/detail.html', context)

