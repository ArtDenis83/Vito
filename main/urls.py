from django.urls import path
from .views import  index, \
                    other_page, \
                    BBLoginView, \
                    BBLogoutView, \
                    profile, \
                    ChangeUserInfoView, \
                    BBPasswordChangeView, \
                    RegisterUserView, \
                    RegisterDoneView, \
                    user_activate, \
                    DeleteUserView, \
                    by_rubric


app_name = "main"
urlpatterns=[
    # Контроллер объявлений из выбранной рубрики
    path('<int:pk>/', by_rubric, name='by_rubric'),
    # Конструктор страниц
    path('<str:page>/', other_page, name='other'),
    # Главная страница
    path('', index, name='index'),
    # путь шаблона "accounts/*/", так как это путь по умолчанию в Django
    path('accounts/login/', BBLoginView.as_view(), name="login"),
    path('accounts/logout/', BBLogoutView.as_view(), name="logout"),
    # Активация пользователя
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    # Сообщение об успешной регистрации
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    # Регистрация
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    # Изменение пароля
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    # Удаление пользователя
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    # Изменение основных данных
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    # Профиль пользователя
    path('accounts/profile/', profile, name="profile"),
]