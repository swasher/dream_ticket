from django.contrib import admin

from stockroom.models import Product, Comment

admin.site.register(Product)
admin.site.register(Comment)