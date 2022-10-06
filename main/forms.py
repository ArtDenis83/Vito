from django import forms
from .models import AdvUser

class ChangeUserInfoForm(forms.ModelForm):
    # Для поля email полное объявление, так как оно должно быть обязательным для заполнения
    email = forms.EmailField(required=True, label="Адрес электронной почты")

    class Meta:
        model=AdvUser
        # остальные поля default, поэтому быстрое объявление
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages' )