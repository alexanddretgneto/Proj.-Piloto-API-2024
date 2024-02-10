# from django.contrib import admin
# from .models import MenuItem, Category

# class MenuItemAdmin(admin.ModelAdmin):
#     list_display = ('title', 'price', 'category')

# admin.site.register(MenuItem, MenuItemAdmin)
# admin.site.register(Category)

from django.contrib import admin
from .models import MenuItem, Category

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category')

admin.site.register(MenuItem, MenuItemAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Adicione outros campos, se desejar

admin.site.register(Category, CategoryAdmin)