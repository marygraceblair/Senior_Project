import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
# from .models import Food, Receipt, Survey
from .models import Food, ListItem, Receipt, Survey, ItemResults

import datetime 
import json
import requests

# im = Image.open("target.jpg") # the second one
# im = im.filter(ImageFilter.MedianFilter())
# enhancer = ImageEnhance.Contrast(im)
# im = enhancer.enhance(2)
# im = im.convert('1')
# im.save('temp2.jpg')

def make_survey(receipt):
    print('making survey')
    currentSurvey = Survey.objects.create()
    print('getting items')
    for item in ListItem.objects.filter(receipt=receipt):
       item_results= ItemResults.objects.create(food = item.food, price=item.price, amount_purchased=item.amount, survey=currentSurvey )
       print('getting item' + str(item.food.name))

def scan_receipt(image):
    text = pytesseract.image_to_string(Image.open(image))

    foods = []
    api_token = 'QfXWHLzym19sLkKqqK9WS7LsUMtuFGUGE9Trgu2k'
    api_url_base = 'https://api.nal.usda.gov/ndb/search/?format=json'

    api_url = api_url_base + api_token

    parameters = {'q': '',
                  'max': '25',
                  'offset': '1',
                  'ds': 'Standard Reference',
                  'api_key': api_token}

    common_reciept_words = ['great', 'fuel', 'points',
                            'per', 'balance', 'cash', 'change', 'number', 'items', 'savings',
                            'pc', 'dillon', 'plus', 'customer', 'pc', 'ml', 'lb', 'sc', 'store', 'total',
                            'purchase', 'low', 'one', 'go', 'grand', 'coupons', 'of', 'dbl']

    dillons_receipt_words = ('tell us how we are doing! earn 50 bonus fuel '
                             'points. plus, enter our monthly sweepstakes: for one of '
                             '100 - $100 gift cards and one $5,000 gift card grand '
                             'prize! go to www.krogerfeedback.com within 7 days.'
                             'enter the information below')
    dillons_receipt_words = dillons_receipt_words.split()
    full_list_words = text.split()

    currentReceipt = Receipt.objects.create()
    #currentFood = None
    currentListItem = None
    currentPrice = 0
    currentAmount = 1
    for index, word in enumerate(full_list_words):

        # if word already in foods, don't add
        # i think i should get rid of this
        #if word in foods:
        #    continue

        if word in dillons_receipt_words:
            continue

        # exit if digit in the string
        if (not word.isalpha()):
            if word == '@':
                # get the quantity
                print('what am i printing here', end=' ')
                if full_list_words[index - 1] == 'lb':
                    #if currentListItem is not None:
                    print('got an amount' + full_list_words[index - 2])
                    #    currentListItem.amount = float(full_list_words[index - 2])
                    currentAmount = float(full_list_words[index - 2])
                else:
                    #if currentListItem is not None:
                    #    currentListItem.amount = float(full_list_words[index - 1])
                    print('got an amount'+ full_list_words[index - 1])
                    currentAmount = float(full_list_words[index - 1])
            continue

        if word == 'B':
            # get the price
            print('food price recognized: ', end=" ")
            # there is a chance to error out here
            # update the ListItem with a price
            if currentListItem is not None:
                currentListItem.price = float(full_list_words[index - 1])
                print(full_list_words[index - 1])
                currentListItem.save()

            # how to go backwards

        # exit if the word is 1 character long
        if (len(word) <= 1):
            continue

        word = word.lower()
        if word in common_reciept_words:
            continue

        parameters['q'] = word
        response = requests.get(api_url_base, params=parameters)
        data = response.json()

        if 'errors' not in data:
            foods.append(word)

            #check whether or not the food item is in my database
            food_ex, created = Food.objects.get_or_create(name=word)

            #now that i have a food, create a listItem for it
            if created:
                currentFood = food_ex
                currentPrice = 0
                list_item = ListItem.objects.create(food = food_ex, receipt=currentReceipt, amount=currentAmount, price=currentPrice)
                currentAmount = 1
                currentListItem = list_item
                print('list item changed to not none')


        print(word)
    print(foods)
    return(foods)
