from django.contrib import admin

# Register your models here.
from transfer.models import Category, Transfer


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

class TransferAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'status']
    list_filter = ['status','category']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Transfer,TransferAdmin)