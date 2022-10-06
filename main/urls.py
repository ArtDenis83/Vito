from django.urls import path
from .views import  index, \
                    other_page, \
                    BBLoginView, \
                    BBLogoutView, \
                    profile, \
                    ChangeUserInfoView, \
                    BBPasswordChangeView


app_name = "main"
urlpatterns=[
    # Конструктор страниц
    path('<str:page>/', other_page, name='other'),
    # Главная страница
    path('', index, name='index'),
    # путь шаблона "accounts/*/", так как это путь по умолчанию в Django
    path('accounts/login/', BBLoginView.as_view(), name="login"),
    path('accounts/logout/', BBLogoutView.as_view(), name="logout"),
    # Изменение пароля
    path('accounts/password/change', BBPasswordChangeView.as_view(), name='password_change'),
    # Изменение основных данных
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name="profile"),
]