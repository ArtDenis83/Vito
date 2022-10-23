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
                    by_rubric, \
                    detail, \
                    profile_bb_detail, \
                    profile_bb_add


app_name = "main"
urlpatterns=[
    # Активация пользователя
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    # Сообщение об успешной регистрации
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    # Регистрация
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', BBLogoutView.as_view(), name="logout"),
    # Изменение пароля
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    # Удаление пользователя
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    # Изменение основных данных
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    # Страница добавления объявления
    path('accounts/profile/add/', profile_bb_add, name='profile_bb_add'),
    # Страница конкретного объявления пользователя
    path('accounts/profile/<int:pk>/', profile_bb_detail, name='profile_bb_detail'),
    # Профиль пользователя
    path('accounts/profile/', profile, name="profile"),
    # путь шаблона "accounts/*/", так как это путь по умолчанию в Django
    path('accounts/login/', BBLoginView.as_view(), name="login"),
    # сведения о выбранном объявлении
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    # объявления из выбранной рубрики
    path('<int:pk>/', by_rubric, name='by_rubric'),
    # Конструктор страниц
    path('<str:page>/', other_page, name='other'),
    # Главная страница
    path('', index, name='index'),
]