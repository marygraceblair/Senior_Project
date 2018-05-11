from django.shortcuts import render
import io
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import redirect 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from . import practice
from .models import Receipt, Food, ListItem, Inventory, Survey, ItemResults
from .forms import AddListItem, InventoryForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms import modelformset_factory, Textarea
import json
from chartit import DataPool, Chart
import random
import datetime
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from chartit import DataPool, Chart

def simple_upload(request):
    if request.method == 'POST':
        image = request.FILES['myfile']
        practice.scan_receipt(image)
        #ListItem.objects.get(receipt=Receipt.objects.latest('date'))
        #receipt=Receipt.objects.latest('date')
        #listitem = ListItem.objects.filter(receipt=receipt) 
        #return render(request, '../templates/corrections.html', {'listitem': listitem})

        model = ListItem
        receipt=Receipt.objects.latest('date')
        inventory = ListItem.objects.filter(receipt=receipt) 
        form = InventoryForm(data = request.POST)
        if form.is_valid():
            form.save()
        else:
            form = InventoryForm()
        context = RequestContext(request)
        return redirect('add')
    return render(request, '../templates/import.html')

def app_entry(request):
    return render(request, '../templates/index.html')
# Create your views here.

def create_survey(request):
    receipt = Receipt.objects.latest('date')
    practice.make_survey(receipt)
    return render(request, '../templates/index.html')

def take_survey(request):
    FoodFormSet = modelformset_factory(ItemResults, fields=('food', 'amount_purchased', 'amount_consumed', 'id'), exclude=['survey', 'price', 'amount_wasted', 'percent_wasted', 'money_wasted'] )
    if request.method == 'POST':
        formset = FoodFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.amount_wasted= instance.amount_purchased - instance.amount_consumed
                instance.percent_wasted = instance.amount_wasted /instance.amount_purchased
                instance.money_wasted = instance.price * instance.percent_wasted
                instance.save()
            receipt = Receipt.objects.latest('date')
            inventory = ListItem.objects.filter(receipt=receipt) 
            survey = Survey.objects.latest('date') 
            total_cost = 0
            total_money_wasted = 0
            total_percent_wasted = 0 #MONEY
            #it's better to redo total stuff here
            for item in inventory:
                total_cost += item.price
            inventory_results = ItemResults.objects.filter(survey=survey)
            for item in inventory_results:
                total_money_wasted += item.money_wasted 

            survey.total_money_wasted = total_money_wasted
            survey.save()
            survey.total_percent_wasted = total_money_wasted / total_cost 
            # i think one of the above will be a float
            #survey total percent wasted is MONEY
            survey.save()
            # item.delete()
            return redirect('delete')
            # do something.
    else:
        formset = FoodFormSet()
    return render(request, '../templates/add.html', {'formset': formset})

def delete(request):
    if request.method == 'POST':
        form = InventoryForm()
        item_id = int(request.POST.get('item_id'))  
        item = ListItem.objects.get(id=item_id)       
        receipt = Receipt.objects.latest('date')
        inventory = ListItem.objects.filter(receipt=receipt) 
        item.delete()
        return render(request,'../templates/corrections.html', {'listitem':inventory })
    receipt=Receipt.objects.latest('date')
    inventory = ListItem.objects.filter(receipt=receipt) 
    return render(request,'../templates/corrections.html', {'listitem':inventory })


def items(request):
    if request.method == 'POST':
        form = InventoryForm()
        item_id = int(request.POST.get('item_id'))  
        item = ListItem.objects.get(id=item_id)       
        receipt = Receipt.objects.latest('date')
        inventory = ListItem.objects.filter(receipt=receipt) 
        item.delete()
        return render(request,'../templates/corrections.html', {'listitem':inventory })
    receipt=Receipt.objects.latest('date')
    inventory = ListItem.objects.filter(receipt=receipt) 
    return render(request, '../templates/items.html', {'listitem': inventory})

def show_inventory(request):
    receipt=Receipt.objects.latest('date')
    inventory = ListItem.objects.filter(receipt=receipt) 
    return render(request,'../templates/items.html', {'listitem': inventory})

def add(request):
    ListItemFormSet = modelformset_factory(ListItem, fields=('food', 'amount', 'price', 'receipt', 'id') )
    if request.method == 'POST':
        formset = ListItemFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
            receipt = Receipt.objects.latest('date')
            inventory = ListItem.objects.filter(receipt=receipt) 
            # item.delete()
            return redirect('delete')
            # do something.
    else:
        formset = ListItemFormSet()
    return render(request, '../templates/add.html', {'formset': formset})

def additem(request):
    if request.method == 'POST':
        item_id = int(request.POST.get('new-listitem'))  
        # item = ListItem.objects.get(id=item_id)       
        receipt = Receipt.objects.latest('date')
        inventory = ListItem.objects.filter(receipt=receipt) 
        # item.delete()
        return render(request,'../templates/corrections.html', {'listitem':inventory })
    receipt=Receipt.objects.latest('date')
    inventory = ListItem.objects.filter(receipt=receipt) 

def remove_items(request):
    if request.method == 'POST':
        form = InventoryForm()
        inventory = Inventory.objects.all()
        item_id = int(request.POST.get('item_id'))  
        item = Inventory.objects.get(id=item_id)       
        item.delete()
        return render_to_response('inventory.html', {
            'form':form, 'inventory':inventory, 
            }, RequestContext(request))

def survey_chart_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    data = \
        DataPool(
           series=
            [{'options': {
               'source': Survey.objects.all()},
              'terms': [
                'date',
                'total_percent_wasted',
                ]}
             ])
    #Step 2: Create the Chart object
    cht = Chart(
            datasource = data,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'date': [
                    'total_percent_wasted']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Total Money Wasted Per Survey'},
               'xAxis': {
                    'title': {
                       'text': 'Date of Survey'}}})
    return render(request, '../templates/survey_chart.html', {'weatherchart': cht})

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


def simple(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': Survey.objects.all()},
              'terms': [
                'date',
                'total_percent_wasted',
                ]}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = weatherdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'date': [
                    'total_percent_wasted',
                    ]
                  }}],
            chart_options =
              {'title': {
                   'text': 'TotalPercentWasted'},
               'xAxis': {
                    'title': {
                       'text': 'Date '}}})

    #Step 3: Send the chart object to the template.
    return render(request, '../templates/survey_chart.html',{'weatherchart': cht})
