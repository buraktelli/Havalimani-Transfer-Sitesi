from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from car.models import Category, Car, Images, Comment, Reservation


class CarImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'price', 'status']
    readonly_fields = ('image_tag',)#'catimg_tag' var hocanınkinde
    list_filter = ['status', 'category']
    inlines = [CarImageInline]
    prepopulated_fields = {'slug': ('title',)}

class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'car', 'image_tag']
    readonly_fields = ('image_tag',)

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Car,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Car,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'rate', 'car', 'user', 'status']
    list_filter = ['status']

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['car', 'user', 'start_from', 'destination_to', 'distance', 'total', 'date', 'time', 'price', 'status']
    list_filter = ['status']

admin.site.register(Category, CategoryAdmin2)
admin.site.register(Car, CarAdmin)
admin.site.register(Images, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reservation, ReservationAdmin)