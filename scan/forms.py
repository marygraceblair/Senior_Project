from django.forms import ModelForm, modelformset_factory
from django import forms
from .models import Inventory, ListItem

class AddListItem(ModelForm):
    class Meta:
        model = ListItem
        fields = '__all__'
        #name = forms.CharField(label='name', max_length=100) 
        # amount = forms.FloatField(required=False, max_value=10, min_value=0, 
        # widget=forms.NumberInput(attrs={'id': 'amount', 'step': "0.01"}))
        # price = forms.FloatField(required=False, max_value=10, min_value=0, 
        # widget=forms.NumberInput(attrs={'id': 'amount', 'step': "0.01"}))

class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
