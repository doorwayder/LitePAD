from django.db import models
from django.contrib.auth.models import User
from orders.singleton_model import SingletonModel
from colorfield.fields import ColorField


class BaseInfo(SingletonModel):
    site_url = models.URLField(verbose_name='Website url', max_length=50)
    title = models.CharField(verbose_name='Title', max_length=20)
    email = models.CharField(verbose_name='Email', max_length=30)
    address = models.CharField(verbose_name='Address', max_length=100)

    def __str__(self):
        return 'Настройки сайта'

    class Meta:
        verbose_name = '_Основные настройки'
        verbose_name_plural = '_Основные настройки'


class ProductCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=150, blank=True, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    color = ColorField(default='#6c757d')
    text_color = ColorField(default='#ffffff')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Order(models.Model):
    time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Время')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.IntegerField(blank=True, verbose_name='Скидка')
    pay_type = models.BooleanField(verbose_name='Наличные')
    cost = models.IntegerField(verbose_name='Сумма')
    description = models.CharField(max_length=100, blank=True, verbose_name='Примечание')

    class Meta:
        ordering = ['-time']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)


class OrderDetail(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Состав заказа'
        verbose_name_plural = 'Состав заказа'


class MaterialCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория сырья'
        verbose_name_plural = 'Категории сырья'


class Material(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=150, blank=True, verbose_name='Описание')
    units = models.CharField(max_length=50, verbose_name='Единицы измерения')
    category = models.ForeignKey(MaterialCategory, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сырье'
        verbose_name_plural = 'Сырье'


class Sostav(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество')

    class Meta:
        unique_together = ['product_id', 'material_id']
        verbose_name = 'Состав'
        verbose_name_plural = 'Состав'

    def __str__(self):
        return self.product_id.name + ' - ' + self.material_id.name + ': ' + str(self.count)
