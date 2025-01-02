# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.intro, name='intro'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='intro'), name='logout'),
    path('add_to_cart/<int:food_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('clear_orders/', views.clear_orders, name='clear_orders'),
    path('booking_success/', views.booking_success, name='booking_success'),  
    path('book_table/', views.book_table, name='book_table'),  
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'), 
    path('bookedtables/',views.bookedtables,name="bookedtables"), 
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
