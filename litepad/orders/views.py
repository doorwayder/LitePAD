from django.shortcuts import render, redirect
from django.utils.timezone import datetime, timedelta
from django.db.models import Sum, F
from .models import Product, ProductCategory, Order, OrderDetail
from .forms import NewOrderForm, OrdersForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
import operator


def neworder(request):
    if request.method == 'POST':
        form = NewOrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(**form.cleaned_data)
            for post_item in form.data:
                if post_item.isdigit():
                    OrderDetail.objects.create(order_id=order, product_id=Product.objects.get(pk=int(post_item)),
                                               count=int(form.data[post_item]))
    else:
        form = NewOrderForm()
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    data = {
        'title': 'Новый заказ',
        'products': products,
        'categories': categories,
        'form': form,
    }
    return render(request, 'orders/neworder.html', data)


def orders(request):
    orders_data = []
    date_range = None
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.data['startdate'] != '' and form.data['stopdate'] != '':
            start = datetime.strptime(form.data['startdate'], "%Y-%m-%d")
            stop = datetime.strptime(form.data['stopdate'], "%Y-%m-%d") + timedelta(minutes=1439)
            orders_data = Order.objects.filter(time__range=(start, stop)).order_by('-time')
            date_range = 'c ' + start.strftime('%d.%m.%Y') + ' по ' + stop.strftime('%d.%m.%Y')  # string of DATE range
    else:
        form = OrdersForm()
    data = {
        'title': 'Заказы',
        'orders': orders_data,
        'form': form,
        'date_range': date_range,
    }
    return render(request, 'orders/orders.html', data)


def statorders(request):
    orders_data = []
    products_data = []
    materials_data = []
    shaurma_count = 0
    coffee_count = 0
    drink_count = 0
    adv_count = 0
    disc_count = 0
    sum_all = 0
    sum_cash = 0
    sum_acq = 0
    date_range = None
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.data['startdate'] != '' and form.data['stopdate'] != '':
            start = datetime.strptime(form.data['startdate'], "%Y-%m-%d")
            stop = datetime.strptime(form.data['stopdate'], "%Y-%m-%d") + timedelta(minutes=1439)
            orders_data = Order.objects.filter(time__range=(start, stop))   # result ORDER_DATA variable (time range)

            result = OrderDetail.objects.filter(order_id__in=orders_data.values('id'), product_id__category=1).values('count').aggregate(sum=Sum('count'))['sum']
            if result is not None:
                shaurma_count = result
            result = OrderDetail.objects.filter(order_id__in=orders_data.values('id'), product_id__category=2).values('count').aggregate(sum=Sum('count'))['sum']
            if result is not None:
                coffee_count = result
            result = OrderDetail.objects.filter(order_id__in=orders_data.values('id'), product_id__category=3).values('count').aggregate(sum=Sum('count'))['sum']
            if result is not None:
                drink_count = result
            result = OrderDetail.objects.filter(order_id__in=orders_data.values('id'), product_id__category=4).values('count').aggregate(sum=Sum('count'))['sum']
            if result is not None:
                adv_count = result
            result = OrderDetail.objects.filter(order_id__in=orders_data.values('id'), product_id__category=5).values('count').aggregate(sum=Sum('count'))['sum']
            if result is not None:
                disc_count = result
            sum_all = orders_data.aggregate(sum=Sum(F('cost')))['sum']
            sum_cash = orders_data.filter(pay_type=True).aggregate(sum=Sum(F('cost')))['sum']
            sum_acq = orders_data.filter(pay_type=False).aggregate(sum=Sum(F('cost')))['sum']
            date_range = 'c ' + start.strftime('%d.%m.%Y') + ' по ' + stop.strftime('%d.%m.%Y') # string of DATE range

            result = OrderDetail.objects.filter(order_id__in=orders_data.values('id'), product_id__category_id=1).order_by('product_id').values('product_id', 'product_id__name','count')
            shaurma = calculate_prod(result)
            result = OrderDetail.objects.filter(order_id__in=orders_data.values('id'), product_id__category_id=2).order_by('product_id').values('product_id', 'product_id__name', 'count')
            coffee = calculate_prod(result)
            result = OrderDetail.objects.filter(order_id__in=orders_data.values('id'), product_id__category_id=3).order_by('product_id').values('product_id', 'product_id__name', 'count')
            drink = calculate_prod(result)
            result = OrderDetail.objects.filter(order_id__in=orders_data.values('id'), product_id__category_id=4).order_by('product_id').values('product_id', 'product_id__name', 'count')
            adv = calculate_prod(result)
            result = OrderDetail.objects.filter(order_id__in=orders_data.values('id'), product_id__category_id=5).order_by('product_id').values('product_id', 'product_id__name', 'count')
            disc = calculate_prod(result)
            products_data.append(shaurma)
            products_data.append(coffee)
            products_data.append(drink)
            products_data.append(adv)
            products_data.append(disc)  # result PRODUCTS_DATA variable

            # MATERIALS calculating
            result = OrderDetail.objects.filter(order_id__in=orders_data.values('id')).values('product_id__sostav__material_id', 'product_id__sostav__material_id__name', 'product_id__sostav__count', 'count').order_by('product_id__sostav__material_id')
            materials_data = calculate_materials(result)

    else:
        form = OrdersForm()
    data = {
        'title': 'Заказы',
        'orders': orders_data,
        'products': products_data,
        'materials': materials_data,
        'shaurma': shaurma_count,
        'coffee': coffee_count,
        'drink': drink_count,
        'adv': adv_count,
        'disc': disc_count,
        'form': form,
        'sum_all': int(0 if sum_all is None else sum_all),
        'sum_cash': int(0 if sum_cash is None else sum_cash),
        'sum_acq': int(0 if sum_acq is None else sum_acq),
        'date_range': date_range,
    }
    return render(request, 'orders/stat.html', data)


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('neworder')
    else:
        form = AuthenticationForm()
    data = {
        'form': form,
    }
    return render(request, 'orders/login.html', data)


def user_logout(request):
    logout(request)
    return redirect('login')


def calculate_prod(details):
    products = list(details)
    i = 0
    while i < len(products):
        j = i + 1
        while j < len(products):
            if products[i]['product_id'] == products[j]['product_id']:
                products[i]['count'] += products[j]['count']
                products.pop(j)
                j -= 1
            j += 1
        i += 1
    products.sort(key=operator.itemgetter(('count')), reverse=True)
    return products


def calculate_materials(details):
    materials = list(details)
    i = 0
    while i < len(materials):
        j = i + 1
        while j < len(materials):
            if materials[i]['product_id__sostav__material_id'] == materials[j]['product_id__sostav__material_id']:
                materials[i]['count'] += materials[j]['count']
                materials.pop(j)
                j -= 1
            j += 1
        i += 1
    return materials
