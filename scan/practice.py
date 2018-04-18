import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

import json
import requests

# im = Image.open("target.jpg") # the second one 
# im = im.filter(ImageFilter.MedianFilter())
# enhancer = ImageEnhance.Contrast(im)
# im = enhancer.enhance(2)
# im = im.convert('1')
# im.save('temp2.jpg')
def scan_receipt(image):
    text = pytesseract.image_to_string(Image.open(image))

    foods = []
    api_token = 'QfXWHLzym19sLkKqqK9WS7LsUMtuFGUGE9Trgu2k'
    api_url_base = 'https://api.nal.usda.gov/ndb/search/?format=json'   

    api_url = api_url_base + api_token

    parameters = { 'q': '',
               'max': '25',
               'offset': '1',
                'ds' : 'Standard Reference',
              'api_key': api_token }
        
    common_reciept_words = ['great', 'fuel', 'points', 
                            'per', 'balance', 'cash', 'change', 'number', 'items', 'savings',
                            'pc', 'dillon', 'plus', 'customer', 'pc', 'ml', 'lb', 'sc','store', 'total',
                            'purchase', 'low', 'one', 'go', 'grand', 'coupons', 'of', 'dbl']

    dillons_receipt_words = 'tell us how we are doing! earn 50 bonus fuel points. plus, enter our monthly sweepstakes: for one of 100 - $100 gift cards and one $5,000 gift card grand prize! go to www.krogerfeedback.com within 7 days. enter the information below'
    dillons_receipt_words = dillons_receipt_words.split()
    full_list_words = text.split()
    for index, word in enumerate(full_list_words):
        
        #if word already in foods, don't add
        if word in foods:
            continue

        if word in dillons_receipt_words:
            continue

        #exit if digit in the string
        if (not word.isalpha()):
            if word == '@':
                print(full_list_words[index-1])
            continue

        if word == 'B':
            print('food price recognized: ', end=" ")
            #there is a chance to error out here
            print(full_list_words[index-1])
            #how to go backwards


        #exit if the word is 1 character long 
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
        print(word)
    print(foods)

