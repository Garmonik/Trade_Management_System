from django import forms


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
