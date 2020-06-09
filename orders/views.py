from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages

from .models import (Topping, Menu_Item, Profile,
Extras, Order, OrderItem,  User, )

import datetime

# Create your views here.

""" user profile view"""
@login_required()
def profile(request):

    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)


    context = { 'my_orders': my_orders, 'user': request.user}

    return render(request, "orders/profile.html", context)

""" view for all orders summary"""
def allorders(request):

    profiles = Profile.objects.all()
    all_orders = Order.objects.filter(is_ordered=True)

    context = { 'all_orders': all_orders}

    return render(request, "orders/allorders.html", context)

""" menu view """
@login_required()
def index(request):

    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})

    #get all items on menu except toppings and extras
    menu_items = Menu_Item.objects.exclude(category__icontains="Topping") \
    .exclude(category__icontains="Extra")


    #get the ordered items so far
    filtered_orders = Order.objects.filter(owner=request.user.profile,
                                          is_ordered=False)
    current_order_products = []

    item_count = 0

    # if there is any currently ordered items put them in current odered prodects
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.ordered_items.all()
        current_order_products = [menu_item.menu_item for menu_item
                                in user_order_items]

        #get number of items in cart
        item_count = user_order.ordered_items.count()

    context ={

        'current_order_products': current_order_products,
        'item_count': item_count,
        "user": request.user,
        "menu_item": menu_items.order_by('-category')
    }
    return render(request, "orders/index.html", context)

@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id

    #get the menuitem by id  passed through kwargs
    menu_item = Menu_Item.objects.filter(id=kwargs.get('item_id', "")).first() #item id sent from the url

    # get quanitity ordered
    quantity = int(request.POST['quantity'])

    # create orderItem of the selected menu_item X qunatity

    for x in range(quantity):
        order_item = OrderItem.objects.create(menu_item=menu_item)
    # create order associated with the user
        user_order, status = Order.objects.get_or_create(owner=user_profile,
                                                        is_ordered=False)

        user_order.ordered_items.add(order_item)

    if status:
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, f" {quantity} {menu_item.sizes} \
                            {menu_item.name} added to cart")

    return HttpResponseRedirect(reverse('orders:index'))

""" view for customizing pizza and subs and anything customizable """
@login_required()
def customize_order(request, food, *args,**kwargs):

    if request.method == "GET":


        toppings = Menu_Item.objects.filter(category__contains="Topping")

        extras = Extras.objects.all()

        extra_cheese=Extras.objects.filter(name__icontains="cheese")

        menu_items = Menu_Item.objects.all()

        ordered_item = Menu_Item.objects.filter(name=food).first()

        context ={

                "ordered_item": ordered_item,
                "user": request.user,
                "menu_item": menu_items,
                "toppings": toppings,
                "extras": extras,
                'extra_cheese': extra_cheese

            }
        return render(request, "orders/customize_order.html", context)


    """ if method is POST """
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id

    menu_item = Menu_Item.objects.filter(name=food).first()
    print (f"this is menu item in get {menu_item}")


    #get toppings depening on number of toppings from form
    toppings = []

    if "Special" in food:
        special_toppings = request.POST.getlist('special_toppings')
        print(f"special_toppings:{special_toppings} \n")
        toppings = special_toppings

        if len(toppings) < 4:

            messages.info(request, "You chose less than 3 toppings! \
             A special pizza needs \
            4 or more toppings! ")
            # get all menu items
            menu_items = Menu_Item.objects.all()
            toppings = Menu_Item.objects.filter(category__contains="Topping")
            menu_items = Menu_Item.objects.all()
            ordered_item = Menu_Item.objects.filter(name=food).first()

            context ={

                    "ordered_item": ordered_item,
                    "user": request.user,
                    "menu_item": menu_items,
                    "toppings": toppings,

                }
            return render(request, "orders/customize_order.html", context)



    if "Special" not in food and "Pizza" in food:
        topping1 = request.POST["topping1"]
        toppings.append(topping1)

        try:
            topping2 = request.POST["topping2"]
            toppings.append(topping2)
        except MultiValueDictKeyError:
            toppings2 = False

        try:
            topping3 = request.POST["topping3"]
            toppings.append(topping3)

        except MultiValueDictKeyError:
            topping3 = False

    # get the extras
    extras = []

    num_extras = 0

    if menu_item.category == "Subs":
        sub_extras = request.POST.getlist('sub_extras')
        #print(f"sub_extras:{sub_extras} \n")

        for extra in sub_extras:
            extras.append(extra + "+ .50c")
            num_extras += 1

    #using price of sub_extra to get the price of extras

    sub_extra = Menu_Item.objects.get(name="Sub_Extra")

    extra_price = sub_extra.price
    #calculate extra cost for extras
    extras_cost = num_extras * extra_price

    #establish quantity of items ordered
    quantity = int(request.POST['quantity'])
    #print(f"custom quantity:{quantity} \n")

    # create orderItem of the selected menu_item\
    for x in range(quantity):
        #order_item = OrderItem.objects.create(menu_item=menu_item)
        order_item = OrderItem.objects.create(menu_item=menu_item,
        ptoppings=toppings, extras=extras, num_extras=num_extras,
        extras_cost=extras_cost )


        # create order associated with the user
        user_order, status = Order.objects.get_or_create(owner=user_profile,
                                                        is_ordered=False)

        user_order.ordered_items.add(order_item)

    if status:
        user_order.save()

    messages.info(request, f" {quantity} {menu_item.sizes} {menu_item.name} \
                            added to cart")

    return HttpResponseRedirect(reverse('orders:index'))


""" view for deleting items from cart """
@login_required()
def delete_from_cart(request, item_id):

    #get ordered item by id
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    deleted_item = OrderItem.objects.get(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, f" {deleted_item.menu_item.sizes} \
            {deleted_item.menu_item.name}  removed from cart")

    return redirect(reverse('orders:ordersummary'))


""" seperate function for getting the cart for summary and checkout """
@login_required()
def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders with is_ordered = false
        return order[0]
    return 0

""" view for showing the cart with current items """
@login_required()
def order_details(request, **kwargs):

    existing_order = get_user_pending_order(request)
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)

    context = {
        'order': existing_order,
        #'orders': orders
    }
    return render(request, 'orders/ordersummary.html', context)


""" view for confirming current order and checking out """
@login_required()
def checkout(request, **kwargs):
    existing_order = get_user_pending_order(request)

    context = {
        'order': existing_order,
    }

    return render(request, 'orders/checkout.html', context)

""" this view save updates the orders from pending to ordered """
@login_required()
def updaterecords(request, order_id):
    # get the order being processed
    order_to_purchase = Order.objects.filter(pk=order_id).first()

    # update each of the individual ordered_items
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()


    # get all ordered_items in the order and update the entire order
    order_items = order_to_purchase.ordered_items.all()

    # update order- is ordered to true
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    user_profile = get_object_or_404(Profile, user=request.user)

    # get the products from the items / the ordderd products are eqaul to
    order_products = [item.menu_item for item in order_items]

    #adding ordered_products list of objects profiles menu_item field (to a many to many field)
    # the * iteates through all the objects in the list
    user_profile.menu_items.add(*order_products)
    user_profile.save()

    # redirects to users profile so they can see the order
    return redirect(reverse('orders:success'))


""" view for page of succesful order """
@login_required()
def success(request, **kwargs):

    user_profile = get_object_or_404(Profile, user=request.user)
    # get last order
    finished_order = Order.objects.filter(owner=user_profile, is_ordered=True).last()

    context = {
        'order': finished_order,
    }
    return render(request, 'orders/purchase_success.html', context)


def register_view(request):

    if request.method == 'GET':
        return render(request, 'orders/register.html')

    user = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    password_confirmation = request.POST['confirm_password']

    """ validate credentials server side"""
    if not user:
        return render(request, 'orders/register.html',
                        {"message": "No username."})

    if len(user) < 4:
        return render(request, 'orders/register.html',
         {"message": "Username should be longer than 4 characters."})

    if not email:
        return render(request, 'orders/register.html',
        {"message": "Please enter a Proper Email."})

    # Email validation required.
    if not password or not password_confirmation:
        return render(request, 'orders/register.html',
        {"message": "Please enter a valid password."})

    if password != password_confirmation:
        return render(request, 'orders/register.html',
        {"message": "Passwords don't match. Please re-enter passwords"})

    if len(password) < 4 or len(password_confirmation) < 4 :
        return render(request, 'orders/register.html',
        {"message": "Password must be at least 4 charachters long."})

    try:
        User.objects.create_user(user, email, password)
    except:
        return render(request, 'orders/register.html',
        {"message": "Registration failed."})

    if first_name:
        User.first_name = first_name
    if last_name:
        User.last_name = last_name
    return HttpResponseRedirect(reverse('orders:login'))


def login_view(request):

    if request.method == "GET":

        return render(request, "orders/login.html")

    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("orders:index"))
    else:
        return render(request, "orders/login.html",
                {"message": "Invalid credentials."})


def logout_view(request):

    logout(request)

    return render(request, "orders/login.html",
        {"message": "Successfully logged out."})
