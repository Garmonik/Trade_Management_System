from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Product, Market, Place, Storage, Selling, Admin
from .forms import ProductForm, AddToMarketForm, PlaceForm, WriteOffFromStorageForm, AddToStorageForm, ReturnFromMarketForm, SellFromMarketForm, SignUpForm, LoginForm
from .utils import get_token


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
    product = get_object_or_404(Product, id=id, user=request.user)
    product.delete()
    messages.success(request, f'Товар "{product.name}" был удален')
    return redirect('products')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = Product(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                user=request.user
            )
            new_product.save()
            messages.success(request, f'Товар "{new_product.name}" добавлен')
            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'products/add.html', {'form': form})


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
    data = Market.objects.select_related('place', 'product').filter(user=request.user)
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

            place = get_object_or_404(Place, name=place_name, user=request.user)
            product = get_object_or_404(Product, name=product_name, user=request.user)

            storage = Storage.objects.filter(place=place, amount__gte=amount, user=request.user)

            if not storage:
                messages.error(request, 'Недостаточно единиц товара в помещении')
                return render(request, 'market/add.html', {'form': form})

            storage = storage.first()
            storage.amount -= amount
            storage.save()

            market = Market(place=place, product=product, amount=amount, price=price, user=request.user)
            market.save()

            messages.success(request, 'Позиция успешно добавлена на рынок')
            return redirect('market')
    else:
        form = AddToMarketForm()
    return render(request, 'market/add.html', {'form': form})


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


def storage(request):
    data = Storage.objects.select_related('place', 'product').filter(user=request.user)
    return render(request, 'storage/index.html', {'data': data})


def add_to_storage(request):
    if request.method == 'POST':
        form = AddToStorageForm(request.POST)
        if form.is_valid():
            place_name = form.cleaned_data['place']
            product_name = form.cleaned_data['product']
            amount = form.cleaned_data['amount']

            place = get_object_or_404(Place, name=place_name, user=request.user)
            product = get_object_or_404(Product, name=product_name, user=request.user)

            storage = Storage(place=place, product=product, amount=amount, user=request.user)
            storage.save()

            messages.success(request, 'Товар успешно добавлен на склад')
            return redirect('storage')
    else:
        form = AddToStorageForm()
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
                response.set_cookie('refresh_token', refresh_token, max_age=3600*24*30)
                return response
    else:
        form = LoginForm()
    return render(request, 'facecontrol/login.html', {'form': form})


# class LoginView(APIView):
#     parser_classes = [JSONParser]
#
#     def post(self, request):
#         if 'email' not in request.data:
#             return Response({'message': 'Пользователь с таким e-mail не найден'}, status=status.HTTP_400_BAD_REQUEST)
#
#         email = request.data.get('email')
#         if not validate_email(email):
#             return Response({'message': 'Пользователь с таким e-mail не найден'}, status=status.HTTP_400_BAD_REQUEST)
#         if 'password' not in request.data:
#             return Response({'message': 'Неверный пароль'}, status=status.HTTP_400_BAD_REQUEST)
#
#         password = request.data.get('password')
#
#         try:
#             user = User.objects.get(email=email)
#             if not user:
#                 return Response({'message': 'Пользователь с таким e-mail не найден'}, status=status.HTTP_401_UNAUTHORIZED)
#             if not user.check_password(password):
#                 return Response({'message': 'Неверный пароль'}, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as e:
#             sentry_sdk.capture_exception(e)
#             error_log = ErrorLog.objects.create(
#                 path=request.path,
#                 error_message=str(e),
#                 error_traceback=traceback.format_exc(),
#                 status_code=getattr(e, 'status_code', 500)
#             )
#             return Response({'message': 'Пользователь с такими e-mail и паролем не найден'}, status=status.HTTP_401_UNAUTHORIZED)
#         access_token_user, refresh_token_user = generate_tokens_user(email, user.password)
#         response_data = {
#             'message': 'Logged in successfully',
#             'index_name': user.customer.namespace,
#             'email': user.email,
#             'is_admin': user.is_admin,
#             'is_super_admin': user.is_super_admin,
#             'use_sources': user.customer.use_sources,
#             'bot_name': user.customer.bot_name,
#             'hello_message': user.customer.hello_message
#         }
#         if user.is_admin:
#             access_token, refresh_token = generate_tokens(user.customer.admin_key)
#         else:
#             access_token, refresh_token = generate_tokens(user.customer.auth_key)
#         response = Response(response_data, status=status.HTTP_200_OK)
#         response.set_cookie('is_admin', user.is_admin)
#         response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='None')
#         response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='None')
#         response.set_cookie('access_token_user', access_token_user, httponly=True, secure=True, samesite='None')
#         response.set_cookie('refresh_token_user', refresh_token_user, httponly=True, secure=True, samesite='None')
#         return response