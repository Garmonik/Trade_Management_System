from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Product, Market, Place, Storage, Selling
from .forms import ProductForm, AddToMarketForm, PlaceForm, WriteOffFromStorageForm, AddToStorageForm, ReturnFromMarketForm, SellFromMarketForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html', {'name': "Магазин"})


def products(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})


def get_product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/get.html', {'product': product})


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, f'Товар "{product.name}" был удален')
    return redirect('products')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = Product(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description']
            )
            new_product.save()
            messages.success(request, f'Товар "{new_product.name}" добавлен')
            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'products/add.html', {'form': form})


def places(request):
    places = Place.objects.all()
    return render(request, 'places/index.html', {'places': places})


def get_place(request, id):
    place = Place.objects.get(id=id)
    return render(request, 'places/get.html', {'place': place})


def delete_place(request, id):
    place = Place.objects.get(id=id)
    place.delete()
    messages.success(request, f'Помещение "{place.name}" было удалено')
    return redirect('places')


def add_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            location = form.cleaned_data['location']
            place = Place(name=name, description=description, location=location)
            place.save()
            messages.success(request, f'Помещение "{place.name}" было добавлено')
            return redirect('places')
    else:
        form = PlaceForm()
    return render(request, 'places/add.html', {'form': form})


def market(request):
    data = Market.objects.select_related('place', 'product').all()
    return render(request, 'market/index.html', {'data': data})


@csrf_exempt
def add_to_market(request):
    if request.method == 'POST':
        form = AddToMarketForm(request.POST)
        if form.is_valid():
            place_name = form.cleaned_data['place']
            product_name = form.cleaned_data['product']
            amount = form.cleaned_data['amount']
            price = form.cleaned_data['price']

            place = get_object_or_404(Place, name=place_name)
            product = get_object_or_404(Product, name=product_name)

            storage = Storage.objects.filter(place=place, amount__gte=amount)

            if not storage:
                messages.error(request, 'Недостаточно единиц товара в помещении')
                return render(request, 'market/add.html', {'form': form})

            storage = storage.first()
            storage.amount -= amount
            storage.save()

            market = Market(place=place, product=product, amount=amount, price=price)
            market.save()

            messages.success(request, 'Позиция успешно добавлена на рынок')
            return redirect('market')
    else:
        form = AddToMarketForm()
    return render(request, 'market/add.html', {'form': form})


def sell_from_market(request, id):
    market = Market.objects.get(id=id)
    product = market.product
    place = market.place
    form = SellFromMarketForm()

    if request.method == 'POST':
        form = SellFromMarketForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            if market.amount < amount:
                messages.error(request, f'Недостаточно товаров в позиции ({market.amount})')
                return render(request, 'market/sell.html', {'product': product, 'place': place, 'form': form, 'market': market})

            if market.amount > amount:
                market.amount -= amount
                market.save()
            else:
                market.delete()

            selling = Selling(place=market.place, product=market.product, amount=amount, price=market.price)
            selling.save()

            messages.success(request, 'Продажа успешно зафиксирована')
            return redirect('market')

    return render(request, 'market/sell.html', {'product': product, 'place': place, 'form': form, 'market': market})


def market_history(request):
    data = Selling.objects.select_related('place', 'product').all()
    return render(request, 'market/history.html', {'data': data})


def return_from_market(request, id):
    market = Market.objects.get(id=id)
    product = market.product
    place = market.place
    form = ReturnFromMarketForm()

    if request.method == 'POST':
        form = ReturnFromMarketForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            if market.amount < amount:
                messages.error(request, f'Недостаточно товаров в позиции ({market.amount})')
                return render(request, 'market/return.html', {'product': product, 'place': place, 'form': form, 'market': market})

            if market.amount > amount:
                market.amount -= amount
                market.save()
            else:
                market.delete()

            storage = Storage(place=market.place, product=market.product, amount=amount)
            storage.save()

            messages.success(request, 'Товар успешно возвращен на склад')
            return redirect('market')

    return render(request, 'market/return.html', {'product': product, 'place': place, 'form': form, 'market': market})


def storage(request):
    data = Storage.objects.select_related('place', 'product').all()
    return render(request, 'storage/index.html', {'data': data})


def add_to_storage(request):
    if request.method == 'POST':
        form = AddToStorageForm(request.POST)
        if form.is_valid():
            place_name = form.cleaned_data['place']
            product_name = form.cleaned_data['product']
            amount = form.cleaned_data['amount']

            place = get_object_or_404(Place, name=place_name)
            product = get_object_or_404(Product, name=product_name)

            storage = Storage(place=place, product=product, amount=amount)
            storage.save()

            messages.success(request, 'Товар успешно добавлен на склад')
            return redirect('storage')
    else:
        form = AddToStorageForm()
    return render(request, 'storage/add.html', {'form': form})


def write_off_from_storage(request, id):
    storage = Storage.objects.get(id=id)
    product = storage.product
    place = storage.place
    form = WriteOffFromStorageForm()

    if request.method == 'POST':
        form = WriteOffFromStorageForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            if storage.amount < amount:
                messages.error(request, f'Недостаточно товаров на складе ({storage.amount})')
                return render(request, 'storage/write_off.html', {'product': product, 'place': place, 'form': form, 'storage': storage})

            if storage.amount > amount:
                storage.amount -= amount
                storage.save()
            else:
                storage.delete()

            messages.success(request, 'Товар успешно списан')
            return redirect('storage')

    return render(request, 'storage/write_off.html', {'product': product, 'place': place, 'form': form, 'storage': storage})


@require_http_methods(["GET", "POST"])
def transfer_storage(request):
    return HttpResponse('Comming soon...')