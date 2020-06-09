from django.urls import path, re_path

from django.conf.urls import url

from . import views

app_name = 'orders'
#list of urls supported by this app (orders)
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('add-to-cart/<int:item_id>', views.add_to_cart, name="add_to_cart"),
    path('customize_order/str<food>', views.customize_order, name="customize_order"),
    path('ordersummary/', views.order_details, name="ordersummary"),
    path('success/', views.success, name='success'),
    path('item/delete/<item_id>)/', views.delete_from_cart, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('updaterecords/<int:order_id>', views.updaterecords, name='updaterecords'), # redirects to the update
    path('profile', views.profile, name='profile'),
    path('allorders', views.allorders, name='allorders')

]
