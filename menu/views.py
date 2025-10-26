from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem
from .forms import MenuItemForm
from cart.forms import CartAddForm
from cart.cart import Cart
from menu.models import MenuItem

def menu_list(request):
    special_items = MenuItem.objects.filter(category='Special')
    breakfast_items = MenuItem.objects.filter(category='Breakfast')
    main_items = MenuItem.objects.filter(category='Main Course')
    beverage_items = MenuItem.objects.filter(category='Beverages')
    special_menu_items = MenuItem.objects.filter(category = 'SPECIAL', available=True)
    breakfast_menu_items = MenuItem.objects.filter(category='BREAKFAST', available=True)
    main_course_menu_items = MenuItem.objects.filter(category='MAIN MEALS', available=True)
    soft_drink_menu_items = MenuItem.objects.filter(category='SOFTDRINKS & JUICES', available=True)
    light_meal_menu_items = MenuItem.objects.filter(category='LIGHT MEALS', available=True)
    beer_and_cider_menu_items = MenuItem.objects.filter(category='BEER & CIDERS', available=True)
    sandwich_menu_items = MenuItem.objects.filter(category='SANDWICHES', available=True)
    dessert_menu_items = MenuItem.objects.filter(category='DESSERT', available=True)
        
    context = {
        'special_items': special_items,
        'breakfast_items': breakfast_items,
        'main_items': main_items,
        'beverage_items': beverage_items,
        'special_menu_items': special_menu_items,
        'breakfast_menu_items': breakfast_menu_items,
        'main_course_menu_items': main_course_menu_items,
        'dessert_menu_items': dessert_menu_items,
        'soft_drink_menu_items': soft_drink_menu_items,
        'light_meal_menu_items': light_meal_menu_items,
        'beer_and_cider_menu_items': beer_and_cider_menu_items,
        'sandwich_menu_items': sandwich_menu_items,
    }
    return render(request, 'menu/menu_list.html', context)

def menu_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    cart_form = CartAddForm()
    return render(request, 'menu/menu_detail.html', {'item': item, 'cart_form': cart_form})

def menu_create(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'menu/menu_create.html', {'form': form})

def menu_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'menu/menu_edit.html', {'form': form})

def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('menu_list')
    return render(request, 'menu/menu_delete.html', {'item': item})

def menu_download(request):
    items = MenuItem.objects.filter(available=True)
    return render(request, 'menu/menu_download.html', {'items': items})

def add_to_cart(request, pk):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, pk=pk)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=item, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')

def remove_from_cart(request, pk):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, pk=pk)
    cart.remove(item)
    return redirect('cart_detail')

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('menu_list')
    if request.method == 'POST':
        # Handle payment or proof upload here
        cart.clear()
        return redirect('order_success')
    return render(request, 'cart/cart_checkout.html', {'cart': cart})

def order_success(request):
    return render(request, 'cart/order_success.html')   
# Additional views for cart management can be added here
