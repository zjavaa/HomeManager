from django.db import models
from django.utils import timezone
from django.db.models import Sum, F, DecimalField, Case, When
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal, ROUND_HALF_UP
# Create your models here.

class Product(models.Model):
	CATEGORIES = [	('food', 'jedzenie'),
					('cats', 'koty'),
					('travels', 'podróże'),
					('fees', 'opłaty'),
					('health', 'zdrowie'),
					('entertaiment','rozrywka'),
					('others', 'inne'),
					]

	name = models.CharField(max_length=100, unique=True, verbose_name="Nazwa produktu/usługi")
	category = models.CharField(max_length=100, choices=CATEGORIES, verbose_name="Kategoria")

	def __str__(self):
		return self.name

class ExpenseManager(models.Manager):

	def get_monthly_expenses(self, year, month):
		return self.get_queryset().filter(expense_date__year=year, expense_date__month=month).prefetch_related('items', 'items__product')

	def get_total_for_month(self, year, month):
		total = self.get_monthly_expenses(year, month).annotate(
			item_total=Case(
				When(items__weight__isnull=False, items__weight__gt=0,
					then=F('items__weight') * F('items__price')),
				default=F('items__quantity') * F('items__price'),
				output_field=DecimalField(max_digits=6, decimal_places=2))
		).aggregate(
			monthly_total=Coalesce(Sum('item_total'), 0, output_field=DecimalField(max_digits=6, decimal_places=2))
		)['monthly_total']
		return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
	
class Expense(models.Model):
	shop_name = models.CharField("Miejsce zakupy", max_length=100)
	expense_date = models.DateField("Data zakupu", default=timezone.now)

	objects = ExpenseManager()

	@property
	def total_amount(self):
		return sum(item.total_price for item in self.items.all())

	def __str__(self):
		return f"Paragon z sklepu {self.shop_name} z dnia {self.expense_date.strftime('%Y-%m-%d')}"

class ExpenseItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='items')
	weight = models.DecimalField("Waga", max_digits=6, decimal_places=3, null=True, blank=True, validators=[MinValueValidator(0)])
	quantity = models.PositiveIntegerField("Ilość", null=True, blank=True)
	price = models.DecimalField("Cena jednostkowa/kg", default=1.0, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

	def clean(self):
		super().clean()
		if self.weight is None and self.quantity is None:
			raise ValidationError('Musisz podać wagę lub ilość danego produktu')
	
	@property
	def total_price(self):
		if self.weight is not None:
			return self.weight*self.price
		return self.quantity*self.price

class IncomeManager(models.Manager):
	def get_monthly_incomes(self, year, month):
		return self.get_queryset().filter(income_date__year=year, income_date__month=month)

	def get_total_for_month(self, year, month):
		total = self.get_monthly_incomes(year, month).aggregate(monthly_total=Coalesce(Sum('amount'),0, output_field=DecimalField()))['monthly_total']		
		return total

class Income(models.Model):
	source = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	income_date = models.DateField(default=timezone.now)

	objects = IncomeManager()

	@property
	def total_amount(self):
		return sum(item.total_price for item in self.items.all())

	def __str__(self):
		return f"Przychód {self.amount} zł od {self.source} dnia {self.income_date.strftime('%Y-%m-%d')}"

