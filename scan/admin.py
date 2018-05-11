from django.contrib import admin
from .models import Food, Receipt, Survey, ListItem, Inventory, ItemResults

# class FoodAdmin(admin.ModelAdmin):
#     list_display = ( 'name')

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ( 'total_spent', 'date' )


class ListItemAdmin(admin.ModelAdmin):
    list_display = ( 'food', 'receipt', 'price', 'amount' )

class ItemResultAdmin(admin.ModelAdmin):
    list_display = ( 'food', 'price','amount_purchased', 'survey', 'amount_consumed', 'amount_wasted', 'percent_wasted', 'money_wasted' )
admin.site.register(Food)
admin.site.register(Inventory)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Survey)
admin.site.register(ListItem, ListItemAdmin)
admin.site.register(ItemResults, ItemResultAdmin)




# Register your models here.
