# Project 3

Web Programming with Python and JavaScript

Project Overview

In this project, I  built a web application for handling a pizza restaurant’s
online orders. Users are able to browse the restaurant’s menu, add items to
their cart, and submit their orders. Meanwhile, the restaurant owners will be
able to add and update menu items, and view orders that have been placed from
the admin page.

Personal Touch. My personal touch was to add the ability for users to see a
user profile that contains a table showing the details of the user's
previous confirmed orders. User's can access their profile from any page once logged in.
Users do have the ability to see their cart at any moment. Also, the admin can
in theory change the status or any detail of an order during and after the order
is placed through the admin (but I didn't really work on this feature,
 its just a product of the models I used)}

(a special pizza is any pizza with 4 or more toppings; a user cannot add special
   pizza with less than 4 toppings to the cart. they will be ).

ORDER Directory:

Models.py:

This project has the following models:
A. Menu_Item: This model is the architype for any possible item on the menu,
including category, name, price, size.

B. Profile. This is the model for a user profile required to create the user
 profile page.

C. OrderItem: this is the instance of a particular ordered item.

D. Order. This is the model for the complete order with foreign keys to profile
and a manytomany relationship with OrderItems. The order class also
contains methods for retrieving the OrderItems in the order and for calculating
 the total price of the order.

(Also a model for toppings and extras but used tangentially in the logic)


STATIC: folder has styling and some pictures.

Views.py has the following view functions:

1.  Profile:  This is the view used for loading a users particular profile page,
    found at profile.html, which contains a table of the users past orders
    and order_details.

2.  allorders: This view is used for loading the a table that contains the
details of all previous orders. This view satisfies the "Viewing Orders"
requirement, though orders could be viewed separately through the admin page.
 Only admins have access to the link to this page.

3.  Index. This is provides the context for the menu page, index.html.
It includes logic for determining whether an order has been made and the
amount of ordered items.  For all items that do not have toppings or extra,
the item as added directly to the cart by making a post request to then
add_to_cart view. For items with toppings or extras, the user is sent to the
customize order template to choose toppings or extras

4.  add_to_cart: When users click the the button to add an item to the cart,
other than a customizable pizza or sub, a POST request is triggered to this view,
which adds the items ordered to the users Order and redirects back to the menu
 page with a message confirming the items ordered to the user's cart.

5.  customize_order: This view takes get and post requests. A get request is
 made leading the user to the customize_order template when a user clicks the
 customize button on either a pizza with toppings or a sub. The user can the
 choose the toppings or extras (if desired) and the quantity desired of that
 particular item. The template will require the user to choose 1 topping for a
 1 topping pizza, 2 toppings for a 2 topping pizza, 3 toppings for a 3 topping
 pizza, or allow the user to pick an unlimited amount of toppings for a special
 pizza. If the user is adding a sub, the user will have the choice of choosing all
 or none of the extras. When the user adds the item to the cart a post request is
  made and toppings or extras (and the number of extras) are added to the
  ordered_item fields. The user is then redirected to the menu page.

6.  7. 8.   checkout, updaterecords and success views serve the function of
laoding the cart summary, checkout page and order success page. The upon
checkout the ordered items is_ordered field is switched to true confirming
 the item has been ordered.

There are also views for registering, logging in and logging out with server-Side
validation for registering and logging in.

Pizza Directory:
Left this pretty much as it came out of the box. I did not modify the Admin.

Thank you to Matt from JustDjango for the helpful tutorial on
e-commerce with django!
