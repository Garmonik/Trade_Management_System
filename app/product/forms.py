from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from product.models import Admin, ProductType, Product, Place, AdminSettings, Market
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
    type_product = forms.ModelChoiceField(
        queryset=ProductType.objects.all(),
        label='Тип товара',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label=None)


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


class UpdateToMarketForm(forms.Form):
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


class AddToMarketForm(forms.Form):
    product = forms.ModelChoiceField(
            label='Товар',
            queryset=Product.objects.none(),
            required=True,
            widget=forms.Select(attrs={'class': 'form-control'}),
            empty_label=None)
    place = forms.ModelChoiceField(
            label='Помещение',
            queryset=Place.objects.none(),
            required=True,
            widget=forms.Select(attrs={'class': 'form-control'}),
            empty_label=None)
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddToMarketForm, self).__init__(*args, **kwargs)

        if user is not None:
            self.fields['product'].queryset = Product.objects.filter(user=user)
            self.fields['place'].queryset = Place.objects.filter(user=user)


class UpdateAmountToMarketForm(forms.Form):
    market = forms.ModelChoiceField(
        label='Товар',
        queryset=Market.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # Используем readonly здесь
        empty_label=None
    )
    amount = forms.IntegerField(
        label='Количество',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UpdateAmountToMarketForm, self).__init__(*args, **kwargs)

        if user is not None:
            self.fields['market'].queryset = Market.objects.filter(user=user)


class SellFromMarketForm(forms.Form):
    amount = forms.IntegerField(label='Количество', required=True, min_value=1)


class ReturnFromMarketForm(forms.Form):
    amount = forms.IntegerField(label='Количество', required=True, min_value=1)


class AddToStorageForm(forms.Form):
    product = forms.ModelChoiceField(
            label='Товар',
            queryset=Product.objects.none(),
            required=True,
            widget=forms.Select(attrs={'class': 'form-control'}),
            empty_label=None)
    place = forms.ModelChoiceField(
            label='Помещение',
            queryset=Place.objects.none(),
            required=True,
            widget=forms.Select(attrs={'class': 'form-control'}),
            empty_label=None)
    amount = forms.IntegerField(
        label='Количество',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddToStorageForm, self).__init__(*args, **kwargs)

        if user is not None:
            self.fields['product'].queryset = Product.objects.filter(user=user)
            self.fields['place'].queryset = Place.objects.filter(user=user)


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
    username = forms.CharField(label='Телефон', max_length=30, required=True)
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
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', "username")


class LoginForm(forms.Form):
    email = forms.EmailField(label='Почта', max_length=254, help_text='Required. Inform a valid email address.')
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))


class AdminSettingsForm(forms.ModelForm):
    date_min = forms.IntegerField(
        label='Количество дней для снижения цен',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )
    percent_min = forms.IntegerField(
        label='Процент снижения',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )
    data_max = forms.IntegerField(
        label='Количество дней для повышении цен',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )
    percent_max = forms.IntegerField(
        label='Процент повышения',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )
    count_min = forms.IntegerField(
        label='Количество товаров для снижения цен',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )
    count_max = forms.IntegerField(
        label='Количество товаров для повышения цен',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )
    write_off_date = forms.IntegerField(
        label='Количество дней для списания или переноса на склад',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )
    minimum_quantity_of_goods = forms.IntegerField(
        label='Минимальное количество товаров в магазине',
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'size': '20'})
    )

    class Meta:
        model = AdminSettings
        fields = ['date_min', 'percent_min', 'count_min', 'data_max', 'percent_max', 'count_max', 'write_off_date', 'minimum_quantity_of_goods']