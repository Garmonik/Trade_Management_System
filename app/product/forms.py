from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from product.models import Admin
from django.utils.translation import gettext_lazy as _


class ProductForm(forms.Form):
    name = forms.CharField(
        label='Название',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        label='Описание',
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'}))


class PlaceForm(forms.Form):
    name = forms.CharField(
        label='Название',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'})
    )
    description = forms.CharField(
        label='Описание',
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'size': '20'})
    )
    location = forms.CharField(
        label='Расположение',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'})
    )


class AddToMarketForm(forms.Form):
    product = forms.CharField(
        label='Товар',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'})
    )
    place = forms.CharField(
        label='Помещение',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'})
    )
    amount = forms.IntegerField(
        label='Количество',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )
    price = forms.FloatField(
        label='Цена',
        required=True,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )


class SellFromMarketForm(forms.Form):
    amount = forms.IntegerField(label='Количество', required=True, min_value=1)


class ReturnFromMarketForm(forms.Form):
    amount = forms.IntegerField(label='Количество', required=True, min_value=1)


class AddToStorageForm(forms.Form):
    product = forms.CharField(
        label='Товар',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'})
    )
    place = forms.CharField(
        label='Помещение',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'})
    )
    amount = forms.IntegerField(
        label='Количество',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )


class TransferStorageForm(forms.Form):
    source = forms.CharField(
        label='Отправитель',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'})
    )
    destination = forms.CharField(
        label='Получатель',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'})
    )
    amount = forms.IntegerField(
        label='Количество',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )


class WriteOffFromStorageForm(forms.Form):
    amount = forms.IntegerField(
        label='Количество',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=30, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=30, required=True)
    email = forms.EmailField(label='Почта', max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Пароль повторно"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Admin
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )


class LoginForm(forms.Form):
    email = forms.EmailField(label='Почта', max_length=254, help_text='Required. Inform a valid email address.')
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))