from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('home/', views.admin_settings_view, name='home'),

    path('products/', views.products, name='products'),
    path('products/<int:id>/', views.get_product, name='get_product'),
    path('products/<int:id>/delete/', views.delete_product, name='delete_product'),
    path('products/add/', views.add_product, name='add_product'),

    path('market/<int:id>/sell/', views.sell_from_market, name='sell_from_market'),
    path('market/history/', views.market_history, name='market_history'),
    path('market/<int:id>/return/', views.return_from_market, name='return_from_market'),
    path('market/<int:id>/return_all/', views.return_from_market_all, name='return_from_market'),
    path('market/<int:id>/write_off_all/', views.write_off_from_market_all, name='return_from_market'),
    path('market/', views.market, name='market'),
    path('market/add/', views.add_to_market, name='add_to_market'),
    path('market/<int:pk>/', views.update_to_market, name='update_to_market'),
    path('market/update/<int:pk>/', views.update_to_market_new, name='update_to_market_new'),
    path('market/update/amount/<int:pk>/', views.update_amount_to_market, name='update_to_market_amount'),


    path('storage/', views.storage, name='storage'),
    path('storage/add/', views.add_to_storage, name='add_to_storage'),
    path('storage/<int:id>/write-off/', views.write_off_from_storage, name='write_off_from_storage'),

    path('places/', views.places, name='places'),
    path('places/<int:id>/', views.get_place, name='get_place'),
    path('places/<int:id>/delete/', views.delete_place, name='delete_place'),
    path('places/add/', views.add_place, name='add_place'),


    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('recommendations/problems/', views.recommendations_ploblems_view, name='rec_ploblems'),
    path('recommendations/successes/', views.recommendations_successes_view, name='rec_successes'),
    path('recommendations/write-off/', views.recommendations_write_off_view, name='rec_write-off'),
    path('recommendations/replenishment/', views.recommendations_replenishment, name='rec_replenishment'),
    path('recommendations/', views.recommendations_view, name='recommendations'),

    path('graf/selling/', views.SalesGraphAPIView.as_view(), name='sales-graph'),
    path('market/list/', views.MarketListView.as_view(), name='market-list'),

]