from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import AdvUser, SubRubric, SuperRubric
from .apps import user_registered

# Форма изменения пользовательских данных
class ChangeUserInfoForm(forms.ModelForm):
    # Для поля email полное объявление, так как оно должно быть обязательным для заполнения
    email = forms.EmailField(required=True, label="Адрес электронной почты")

    class Meta:
        model=AdvUser
        # остальные поля default, поэтому быстрое объявление
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages' )

# Форма регистрации и валидации пароля
class RegisterUserForm(forms.ModelForm):
    # Обязательные для заполнения поля объявляются явно
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput,
                                # ниже требования к вводимому паролю
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                help_text='Введите тот же пароль еще раз для проверки')

    # Валидация пароля в поле password1 (первый пароль)
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    # Переопределение метода clean для проверки совпадения паролей
    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    # Переопределение метода save() чтобы ввести значения False в поля is_activ*, чтобы user пока не мог войти
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        # Отправка сигнала user_registered для отсылки письма активации
        user_registered.send(RegisterUserForm,instance=user)
        return user

    class Meta:
        model = AdvUser
        # Краткое объявление полей формы
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_messages')


# Форма администрирования подрубрик в админке
class SubRubricForm(forms.ModelForm):
    # Выбор надрубрики обязателен
    super_rubric = forms.ModelChoiceField(queryset=SuperRubric.objects.all(),
                                          empty_label=None,
                                          label='Надрубрика',
                                          required=True)
    class Meta:
        model = SubRubric
        fields = '__all__'


# Форма поиска объявлений
class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')

