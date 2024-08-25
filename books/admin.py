from django.contrib import admin
from . import models

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('cat_Title',)}
    list_display = ('cat_Title', 'slug',)

admin.site.register(models.BookCategory, CategoryAdmin)
admin.site.register(models.Book)
