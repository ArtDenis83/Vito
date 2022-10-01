from django.urls import path
from .views import  index, \
                    other_page, \
                    BBLoginView, \
                    BBLogoutView, \
                    profile


app_name = "main"
urlpatterns=[
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
    # путь шаблона "accounts/*/", так как это путь по умолчанию в Django
    path('accounts/login/', BBLoginView.as_view(), name="login"),
    path('accounts/logout/', BBLogoutView.as_view(), name="logout"),
    path('accounts/profile/', profile, name="profile"),
]