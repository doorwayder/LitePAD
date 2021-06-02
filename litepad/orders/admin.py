from django.contrib import admin
from .models import Order, OrderDetail, Material, Product, ProductCategory, MaterialCategory, Sostav, BaseInfo
from django.db.utils import ProgrammingError


class BaseInfoAdmin(admin.ModelAdmin):
    # Создадим объект по умолчанию при первом страницы SiteSettingsAdmin со списком настроек
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # обязательно оберните загрузку и сохранение SiteSettings в try catch,
        # чтобы можно было выполнить создание миграций базы данных
        try:
            BaseInfo.load().save()
        except ProgrammingError:
            pass

    # запрещаем добавление новых настроек
    def has_add_permission(self, request, obj=None):
        return False

    # а также удаление существующих
    def has_delete_permission(self, request, obj=None):
        return False


class ProductSostavInline(admin.TabularInline):
    model = Sostav


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'color', )
    list_display_links = ('id', 'name', )
    list_filter = ('category', )
    inlines = [ProductSostavInline, ]


class OrderDetailsInline(admin.TabularInline):
    model = OrderDetail


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'user', 'discount', 'pay_type', 'cost', )
    list_display_links = ('id', 'time', )
    inlines = [OrderDetailsInline, ]
    list_filter = ('time',)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


admin.site.register(BaseInfo, BaseInfoAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductsAdmin)
admin.site.register(Material)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(MaterialCategory)
