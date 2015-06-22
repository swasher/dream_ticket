# coding: utf-8
from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование товара')
    slug = models.SlugField(verbose_name='Slug field')
    description = models.TextField(blank=True, null=False, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Стоимость, грн.')
    created_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата занесения')
    modified_at = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name='Дата изменения')