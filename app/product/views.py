import json
from datetime import timedelta

from django.contrib.auth import authenticate, login
from django.db.models import Sum, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Market, Place, Storage, Selling, Admin, AdminSettings, MarketUpdate
from .forms import ProductForm, AddToMarketForm, PlaceForm, WriteOffFromStorageForm, AddToStorageForm, ReturnFromMarketForm, SellFromMarketForm, SignUpForm, LoginForm, AdminSettingsForm, UpdateToMarketForm, UpdateAmountToMarketForm
from .serializers import MarketSerializer
from .utils import get_token


# def home(request):
#     return render(request, 'home.html')


def about(request):
    return render(request, 'about.html', {'name': "Магазин"})


def products(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'products/index.html', {'products': products})


def get_product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/get.html', {'product': product})


def delete_product(request, id):
    product = get_object_or_404(Product, id=id, user=request.user)
    product.delete()
    messages.success(request, f'Товар "{product.name}" был удален')
    return redirect('products')


def add_product(request):
    try:
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                new_product = Product(
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                    user=request.user,
                    type_product=form.cleaned_data['type_product'].name
                )
                new_product.save()
                messages.success(request, f'Товар "{new_product.name}" добавлен')
                return redirect('products')
        else:
            form = ProductForm()
        return render(request, 'products/add.html', {'form': form})
    except:
        return render(request, '404.html')


def places(request):
    places = Place.objects.filter(user=request.user)
    return render(request, 'places/index.html', {'places': places})


def get_place(request, id):
    place = get_object_or_404(Place, id=id, user=request.user)
    return render(request, 'places/get.html', {'place': place})


def delete_place(request, id):
    place = get_object_or_404(Place, id=id, user=request.user)
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
            place = Place(name=name, description=description, location=location, user=request.user)
            place.save()
            messages.success(request, f'Помещение "{place.name}" было добавлено')
            return redirect('places')
    else:
        form = PlaceForm()
    return render(request, 'places/add.html', {'form': form})


def market(request):
    data = Market.objects.select_related('place', 'product').filter(user=request.user).order_by("place__name")
    return render(request, 'market/index.html', {'data': data})


@csrf_exempt
def add_to_market(request):
    if request.method == 'POST':
        form = AddToMarketForm(request.POST, user=request.user)
        if form.is_valid():
            place_name = form.cleaned_data['place'].name
            product_name = form.cleaned_data['product'].name
            amount = form.cleaned_data['amount']
            price = form.cleaned_data['price']

            place = get_object_or_404(Place, name=place_name, user=request.user)
            product = get_object_or_404(Product, name=product_name, user=request.user)

            storage = Storage.objects.filter(place=place, amount__gte=amount, user=request.user)

            if not storage:
                messages.error(request, 'Недостаточно единиц товара в помещении')
                return render(request, 'market/add.html', {'form': form})

            storage = storage.first()
            storage.amount -= amount
            storage.save()

            if market := Market.objects.filter(place=place, product=product, price=price, user=request.user):
                market = market.first()
                market.amount += amount
                market.save()
            else:
                market = Market(place=place, product=product, amount=amount, price=price, user=request.user)
                market.save()

            recent_update_exists = MarketUpdate.objects.create(
                market=market,
                product=market.product)

            messages.success(request, 'Позиция успешно добавлена на рынок')
            return redirect('market')
    else:
        form = AddToMarketForm(user=request.user)
    return render(request, 'market/add.html', {'form': form})


def update_to_market_new(request, pk):
    if request.method == 'POST':
        form = UpdateToMarketForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            price = form.cleaned_data['price']

            market = get_object_or_404(Market, user=request.user, id=pk)
            storage = Storage.objects.filter(place=market.place, amount__gte=amount, user=request.user)

            if not storage:
                messages.error(request, 'Недостаточно единиц товара в помещении')
                return render(request, 'market/update.html', {'form': form})

            storage = storage.first()
            if storage.amount >= amount:
                storage.amount -= amount
            else:
                amount, storage.amount = storage.amount, 0
            storage.save()

            market.amount = amount
            market.price = price
            market.save()

            messages.success(request, 'Позиция успешно добавлена на рынок')
            return redirect('market')
    else:
        form = UpdateToMarketForm()
    market = get_object_or_404(Market, user=request.user, id=pk)
    return render(request, 'market/update.html', {'form': form, "market": market})


def update_to_market(request, id):
    if request.method == 'POST':
        try:
            json_str = request.body.decode('utf-8')
            data_dict = json.loads(json_str)
            price = data_dict.get('new_price')
            market = get_object_or_404(Market, user=request.user, id=id)
            recent_update_exists = MarketUpdate.objects.create(
                market=market,
                product=market.product)
            market.price = price
            market.save()
            return JsonResponse({"success": True, "message": "Цена успешно обновлена"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})


def sell_from_market(request, id):
    market = get_object_or_404(Market, user=request.user, id=id)
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

            selling = Selling(place=market.place, product=market.product, amount=amount, price=market.price, user=request.user)
            selling.save()

            messages.success(request, 'Продажа успешно зафиксирована')
            return redirect('market')

    return render(request, 'market/sell.html', {'product': product, 'place': place, 'form': form, 'market': market})


def market_history(request):
    data = Selling.objects.select_related('place', 'product').filter(user=request.user)
    return render(request, 'market/history.html', {'data': data})


def return_from_market(request, id):
    market = get_object_or_404(Market, user=request.user, id=id)
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

            storage = Storage(place=market.place, product=market.product, amount=amount, user=request.user)
            storage.save()

            messages.success(request, 'Товар успешно возвращен на склад')
            return redirect('market')

    return render(request, 'market/return.html', {'product': product, 'place': place, 'form': form, 'market': market})


def return_from_market_all(request, id):
    try:
        market = get_object_or_404(Market, user=request.user, id=id)
        product = market.product
        place = market.place
        if request.method == 'POST':
            amount = market.amount
            market.delete()

            storage = Storage(place=market.place, product=market.product, amount=amount, user=request.user)
            storage.save()

            return JsonResponse({"success": True, "message": "Товар успешно перенесен на склад."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


def write_off_from_market_all(request, id):
    try:
        market = get_object_or_404(Market, user=request.user, id=id)
        product = market.product
        place = market.place
        if request.method == 'POST':
            market.delete()

            return JsonResponse({"success": True, "message": "Товар успешно списан."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


def write_off_from_market_all_new(request, id):
    market = get_object_or_404(Market, user=request.user, id=id)
    product = market.product
    place = market.place
    if request.method == 'POST':
        amount = market.amount
        market.delete()

        storage = Storage(place=market.place, product=market.product, amount=amount, user=request.user)
        storage.save()

        messages.success(request, 'Товар успешно возвращен на склад')
        return redirect('rec_write-off')


def storage(request):
    data = Storage.objects.select_related('place', 'product').filter(user=request.user).order_by("place__name")
    return render(request, 'storage/index.html', {'data': data})


def add_to_storage(request):
    if request.method == 'POST':
        form = AddToStorageForm(request.POST, user=request.user)
        if form.is_valid():
            place_name = form.cleaned_data['place'].name
            product_name = form.cleaned_data['product'].name
            amount = form.cleaned_data['amount']

            place = get_object_or_404(Place, name=place_name, user=request.user)
            product = get_object_or_404(Product, name=product_name, user=request.user)

            if storage := Storage.objects.filter(place=place, product=product, user=request.user):
                storage = storage.first()
                storage.amount += amount
                storage.save()
            else:
                storage = Storage(place=place, product=product, amount=amount, user=request.user)
                storage.save()

            messages.success(request, 'Товар успешно добавлен на склад')
            return redirect('storage')
    else:
        form = AddToStorageForm(user=request.user)
    return render(request, 'storage/add.html', {'form': form})


def write_off_from_storage(request, id):
    storage = get_object_or_404(Storage, user=request.user, id=id)
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


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            messages.error(request, form.errors)
    else:
        form = SignUpForm()
    return render(request, 'facecontrol/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(Admin, email=form.cleaned_data['email'])
            if not user.check_password(form.cleaned_data['password']):
                messages.error(request, f'Неверный пароль')
                return redirect('/login/')
            else:
                response = redirect('/home/')
                access_token, refresh_token = get_token(user)
                response.set_cookie('access_token', access_token, max_age=3600)
                response.set_cookie('refresh_token', refresh_token, max_age=3600 * 24 * 30)
                return response
    else:
        form = LoginForm()
    return render(request, 'facecontrol/login.html', {'form': form})


def logout_view(request):
    response = redirect('/login/')
    response.set_cookie('access_token', None, max_age=0)
    response.set_cookie('refresh_token', None, max_age=0)
    return response


def admin_settings_view(request):
    settings = get_object_or_404(AdminSettings, user=request.user)
    if request.method == 'POST':
        form = AdminSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return render(request, 'home.html', {'form': form})
    else:
        form = AdminSettingsForm(instance=settings)
    return render(request, 'home.html', {'form': form})


def process_user_markets(request):
    results = []
    try:
        admin_settings = AdminSettings.objects.get(user=request.user)
    except AdminSettings.DoesNotExist:
        return []

    markets = Market.objects.filter(user=request.user)

    date_min = admin_settings.date_min
    count_min = admin_settings.count_min
    percent_min = admin_settings.percent_min

    compare_date = timezone.now() - timedelta(days=date_min)

    for market in markets:
        product = market.product

        total_sold = Selling.objects.filter(
            product=product,
            time__gte=compare_date
        ).aggregate(total=Sum('amount'))['total'] or 0

        if total_sold < count_min:
            new_price = market.price - (market.price * percent_min / 100)
            result = {
                'product': product.name,
                'place': market.place.name,
                'price': market.price,
                'new_price': new_price,
            }
            results.append(result)

    return results


def recommendations_view(request):
    return redirect("rec_replenishment")


def recommendations_ploblems_view(request):
    results = []
    try:
        admin_settings = AdminSettings.objects.get(user=request.user)
    except AdminSettings.DoesNotExist:
        return []

    markets = Market.objects.filter(user=request.user)

    date_min = admin_settings.date_min
    count_min = admin_settings.count_min
    percent_min = admin_settings.percent_min

    compare_date = timezone.now() - timedelta(days=date_min)

    for market in markets:
        product = market.product

        total_sold = Selling.objects.filter(
            product=product,
            time__gte=compare_date
        ).aggregate(total=Sum('amount'))['total'] or 0

        recent_update_exists = MarketUpdate.objects.filter(
            market=market,
            product=product,
            time__gte=compare_date
        ).exists()

        if recent_update_exists:
            continue

        if total_sold < count_min:
            new_price = market.price - (market.price * percent_min / 100)
            result = {
                'product': product.name,
                'place': market.place.name,
                'price': market.price,
                'new_price': new_price,
                'product_id': product.id,
                'place_id': market.place.id,
                'market': market.id
            }
            results.append(result)
    return render(request, 'recommendations/problems.html', {"results": results})


def recommendations_successes_view(request):
    results = []
    try:
        admin_settings = AdminSettings.objects.get(user=request.user)
    except AdminSettings.DoesNotExist:
        return []

    markets = Market.objects.filter(user=request.user)

    date_max = admin_settings.data_max
    count_max = admin_settings.count_max
    percent_max = admin_settings.percent_max

    compare_date = timezone.now() - timedelta(days=date_max)

    for market in markets:
        product = market.product

        total_sold = Selling.objects.filter(
            product=product,
            time__gte=compare_date
        ).aggregate(total=Sum('amount'))['total'] or 0

        recent_update_exists = MarketUpdate.objects.filter(
            market=market,
            product=product,
            time__gte=compare_date
        ).exists()

        if recent_update_exists:
            continue

        if total_sold > count_max:
            new_price = market.price + (market.price * percent_max / 100)
            result = {
                'product': product.name,
                'place': market.place.name,
                'price': market.price,
                'new_price': new_price,
                'product_id': product.id,
                'place_id': market.place.id,
                'market': market.id
            }
            results.append(result)
    return render(request, 'recommendations/successes.html', {"results": results})


def recommendations_write_off_view(request):
    results = []
    try:
        admin_settings = AdminSettings.objects.get(user=request.user)
    except AdminSettings.DoesNotExist:
        return []

    markets = Market.objects.filter(user=request.user)

    write_off_date = admin_settings.write_off_date

    compare_date = timezone.now() - timedelta(days=write_off_date)

    for market in markets:
        product = market.product

        total_sold = Selling.objects.filter(
            product=product,
            time__gte=compare_date
        ).aggregate(total=Sum('amount'))['total'] or 0

        recent_update_exists = MarketUpdate.objects.filter(
            market=market,
            product=product,
            time__gte=compare_date
        ).exists()

        if recent_update_exists:
            continue

        result = {
            'product': product.name,
            'place': market.place.name,
            'price': market.price,
            'product_id': product.id,
            'place_id': market.place.id,
            'market': market.id
        }
        results.append(result)
    return render(request, 'recommendations/write_off.html', {"results": results})


def recommendations_replenishment(request):
    results = []
    try:
        admin_settings = AdminSettings.objects.get(user=request.user)
    except AdminSettings.DoesNotExist:
        return []

    markets = Market.objects.filter(user=request.user)

    minimum_quantity_of_goods = admin_settings.minimum_quantity_of_goods

    for market in markets:
        product = market.product
        if market.amount <= minimum_quantity_of_goods:
            result = {
                'product': product.name,
                'place': market.place.name,
                'amount': market.amount,
                'product_id': product.id,
                'place_id': market.place.id,
                'market': market.id
            }
            results.append(result)
    return render(request, 'recommendations/replenishment.html', {"results": results})


def update_amount_to_market(request, pk):
    if request.method == 'POST':
        form = UpdateAmountToMarketForm(request.POST, user=request.user)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            market = form.cleaned_data['market']

            market = get_object_or_404(Market, id=market.id, user=request.user)
            storage = Storage.objects.filter(place=market.place, amount__gte=amount, user=request.user)

            if not storage:
                messages.error(request, 'Недостаточно единиц товара в помещении')
                return render(request, 'market/add.html', {'form': form})

            storage = storage.first()
            if storage.amount >= amount:
                storage.amount -= amount
            else:
                amount, storage.amount = storage.amount, 0
            storage.save()

            market.amount += amount
            market.save()

            messages.success(request, 'Позиция успешно добавлена на рынок')
            return redirect('rec_replenishment')
    else:
        form = UpdateAmountToMarketForm(user=request.user)
    market = get_object_or_404(Market, id=pk, user=request.user)
    return render(request, 'recommendations/replenishment_update.html', {'form': form, 'market': market})


class SalesGraphAPIView(APIView):

    def get(self, request):
        market_id = request.query_params.get('market', None)
        period = request.query_params.get('period', 'all_time')
        market = get_object_or_404(Market, id=market_id, user=request.user)
        queryset = Selling.objects.filter(user=request.user, place=market.place)
        now = timezone.now()

        if request.query_params.get('date') == 'last_week':
            last_week_start_time = now - timedelta(days=7)
            last_week_end_time = now
            result = {str(last_week_start_time + timedelta(days=i)): 0 for i in range(0, 7, 1)}
            queryset = queryset.filter(time__gte=last_week_start_time, time__lt=last_week_end_time)

            for item in queryset:
                for i in range(7):
                    if last_week_start_time + timedelta(days=i) <= item.time < last_week_start_time + timedelta(days=i + 1):
                        result[str(last_week_start_time + timedelta(days=i))] += item.amount * item.price

            return Response(result, status=status.HTTP_200_OK)

        if request.query_params.get('date') == 'last_month':
            last_month_start_time = now - timedelta(days=30)
            last_month_end_time = now
            result = {str(last_month_start_time + timedelta(days=i)): 0 for i in range(0, 31, 1)}
            queryset = queryset.filter(time__gte=last_month_start_time, time__lt=last_month_end_time)

            for item in queryset:
                for i in range(31):
                    if last_month_start_time + timedelta(days=i) <= item.time < last_month_start_time + timedelta(days=i + 1):
                        result[str(last_month_start_time + timedelta(days=i))] += item.amount * item.price

            return Response(result, status=status.HTTP_200_OK)

        if request.query_params.get('date') == 'last_year':
            last_month_start_time = now - timedelta(days=365)
            last_month_end_time = now
            result = {str(last_month_start_time + timedelta(days=i)): 0 for i in range(0, 365, 1)}
            queryset = queryset.filter(time__gte=last_month_start_time, time__lt=last_month_end_time)

            for item in queryset:
                for i in range(366):
                    if last_month_start_time + timedelta(days=i) <= item.time < last_month_start_time + timedelta(days=i + 1):
                        result[str(last_month_start_time + timedelta(days=i))] += item.amount * item.price

            return Response(result, status=status.HTTP_200_OK)

        if request.query_params.get('date') == 'all_time':
            first_record = queryset.first()
            last_record = queryset.last()

            if not first_record or not last_record:
                return Response({'error': 'No records in the database'})

            start_time = first_record.time.replace(minute=0, second=0, microsecond=0)
            end_time = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
            result = {str(start_time + timedelta(hours=i)): 0 for i in range(0, int((end_time - start_time).total_seconds() / 3600), 1)}
            queryset = queryset.filter(time__gte=start_time, time__lt=end_time)

            for item in queryset:
                for i in range(len(result)):
                    if start_time + timedelta(hours=i) <= item.time < start_time + timedelta(hours=i + 1):
                        result[str(start_time + timedelta(hours=i))] += item.amount * item.price

            return Response(result, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid date parameter'}, status=status.HTTP_400_BAD_REQUEST)


class MarketListView(ListAPIView):
    serializer_class = MarketSerializer

    def get_queryset(self):
        return Market.objects.filter(user=self.request.user).distinct()
