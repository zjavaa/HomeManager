from django import forms
from django.forms import inlineformset_factory
from budget.models import Expense, ExpenseItem

# Tworzenie formset dla pozycji paragonu
ExpenseItemFormSet = inlineformset_factory(
    Expense, 
    ExpenseItem,
    fields=('product', 'weight', 'quantity', 'price'),
    extra=1,
    can_delete=False
)
