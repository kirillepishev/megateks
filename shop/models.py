from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

#Категории оборудования
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    icon = models.CharField(max_length=100, blank=True, verbose_name="Иконка (emoji)")

    class Meta:
        verbose_name = "Категория оборудования"
        verbose_name_plural = "Категории оборудования"

    def __str__(self):
        return self.name

#Товары
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=300, verbose_name="Название оборудования")
    description = models.TextField(verbose_name="Описание")
    specifications = models.TextField(blank=True, verbose_name="Характеристики")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Стоимость")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Наличие на складе")
    is_active = models.BooleanField(default=True, verbose_name="Доступно для заказа")
    manufacturer = models.CharField(max_length=200, blank=True, verbose_name="Производитель")
    article = models.CharField(max_length=100, blank=True, verbose_name="Артикул")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.article})"
    
#Заказы клиентов
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Выполнен'),
        ('canceled', 'Отменен'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Клиент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оформления")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус заказа")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Общая сумма")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

#Позиции заказа 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Количество")
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_item_price(self):
        return self.quantity * self.price_at_time

#Профиль сотрудника
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile', verbose_name="Пользователь")
    position = models.CharField(max_length=100, verbose_name="Должность")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Рабочий телефон")

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"

    def __str__(self):
        return f"Сотрудник: {self.user.username}"