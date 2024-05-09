from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('products/<int:id>/', views.get_product, name='get_product'),
    path('products/<int:id>/delete/', views.delete_product, name='delete_product'),
    path('products/add/', views.add_product, name='add_product'),
    path('market/<int:id>/sell/', views.sell_from_market, name='sell_from_market'),
    path('market/history/', views.market_history, name='market_history'),
    path('market/<int:id>/return/', views.return_from_market, name='return_from_market'),
    path('storage/', views.storage, name='storage'),
    path('storage/add/', views.add_to_storage, name='add_to_storage'),
    path('storage/<int:id>/write-off/', views.write_off_from_storage, name='write_off_from_storage'),
    path('places/', views.places, name='places'),
    path('places/<int:id>/', views.get_place, name='get_place'),
    path('places/<int:id>/delete/', views.delete_place, name='delete_place'),
    path('places/add/', views.add_place, name='add_place'),
    path('market/', views.market, name='market'),
    path('market/add/', views.add_to_market, name='add_to_market'),
    path('transfer-storage/', views.transfer_storage, name='transfer_storage'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]