from django.shortcuts import render
from django.apps import apps
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from budget.models import *
from django.utils import timezone
from budget.forms import ExpenseItemFormSet 
from .mixins import MultipleFormsetsMixin
import pprint


# Create your views here.
class BudgetView(TemplateView):
	template_name = "budget/budget.html"

	def get_context_data(self, **kwargs):
		time = timezone.now()
		month = time.month 
		year = time.year

		context = super().get_context_data(**kwargs)
		context = { 'expenses': Expense.objects.get_monthly_expenses(year, month), 
					'incomes': Income.objects.get_monthly_incomes(year, month),
					'total_month_expenses': Expense.objects.get_total_for_month(year, month),
					'total_month_icomes': Income.objects.get_total_for_month(year, month)
					}
		return context


class ExpenseListView(ListView):
	model = Expense
	context_object_name = 'all_expenses'

class ExpenseCreateView(MultipleFormsetsMixin, CreateView):
	model = Expense
	fields = ['shop_name', 'expense_date']
	template_name = 'budget/expense_form.html'
	success_url = reverse_lazy('expense_list')
	formsets_config = { 'products': { 'formset_class': ExpenseItemFormSet }} 

class ExpenseUpdateView(MultipleFormsetsMixin, UpdateView):
	model = Expense
	fields = ['shop_name', 'expense_date']
	template_name = 'budget/expense_form.html'
	success_url = reverse_lazy('expense_list')
	formsets_config = { 'products': { 'formset_class': ExpenseItemFormSet }} 

class ExpenseDeleteView(DeleteView):
	model = Expense
	template_name = 'budget/delete_confirm.html'
	success_url = reverse_lazy('expense_list')
	
class ProductCreateView(CreateView):
	model = Product
	fields = ['name','category']
	template_name = 'budget/product_form.html'

	def get_success_url(self):
		return self.request.GET.get('next', reverse_lazy('budget'))

class IncomeListView(ListView):
	model = Income
	context_object_name = 'all_incomes'

class IncomeCreateView(CreateView):
	model = Income
	fields = ['source', 'amount', 'income_date']
	template_name = 'budget/income_form.html'
	success_url = reverse_lazy('income_list')

class IncomeDeleteView(DeleteView):
	model = Income
	template_name = 'budget/delete_confirm.hmtl'
	success_url = reverse_lazy('income_list')
