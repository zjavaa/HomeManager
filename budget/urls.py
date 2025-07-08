from django.urls import path
from .views import *

urlpatterns = [
        path("", BudgetView.as_view(), name="budget"),
		path("expense_list", ExpenseListView.as_view(), name='expense_list'),
		path("add_expense", ExpenseCreateView.as_view(), name='expense_create'),
		path("<pk>/update_expense", ExpenseUpdateView.as_view(), name='expense_update'),
		path("<pk>/delete_expense", ExpenseDeleteView.as_view(), name='expense_delete'),
		path("add_product", ProductCreateView.as_view(), name='product_create'),
		path("income_list", IncomeListView.as_view(), name='income_list'),
		path("income_create", IncomeCreateView.as_view(), name='income_create'),
		path("<pk>/delete_income", IncomeDeleteView.as_view(), name='income_delete'),
        ]

