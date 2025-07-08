from django.core.exceptions import ValidationError
from django.views.generic.edit import UpdateView
import pprint

class MultipleFormsetsMixin:
	formsets_config = {}

	def get_formset_extras(self, formset_name, formset_class):
		config = self.formsets_config.get(formset_name, {})
		
		if isinstance(self, UpdateView):
			return config.get('extra_update', 0)
		return config.get('extra_create', 1)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		for formset_name, config in self.formsets_config.items():
			formset_class = config['formset_class']
			formset_class.extra = self.get_formset_extras(formset_name, formset_class)	
			if self.request.POST:
				context[f'{formset_name}_formset'] = formset_class(self.request.POST, instance=self.object, prefix=formset_name)
			else:
				context[f'{formset_name}_formset'] = formset_class(instance=self.object, prefix=formset_name)
		return context

	def form_valid(self, form):
		formsets_dict = {}
		context = self.get_context_data()
		for formset_name in self.formsets_config.keys():
			formsets_dict[formset_name] = context[f'{formset_name}_formset']
		formsets_valid = all([formset.is_valid() for formset in formsets_dict.values()])
		if form.is_valid() and formsets_valid:
			self.object = form.save()
			for formset in formsets_dict.values():
				formset.instance = self.object
				formset.save()
			return super().form_valid(form)
		return self.form_invalid(form)
		
