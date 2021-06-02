from django import forms
from .models import Order, OrderDetail


class NewOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['discount', 'pay_type', 'cost', 'user', 'description']


class OrdersForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['id']
