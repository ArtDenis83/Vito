from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'main/index.html')

# В качестве идентификатора страницы берет имя шаблона без пути и расширения
def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    # Если страница не существует, поднимает ошибку 404
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class BBLoginView(LoginView):
    template_name = 'main/login.html'

# Примесь LoginRequiredMixin дает доступ только пользователю, выполнившему вход
class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'

# Доступ к странице профиля возможен только после регистрации и при выполнении входа
@login_required
def profile(request):
    return render(request, 'main/profile.html')
