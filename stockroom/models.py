# coding: utf-8
from django.db import models
from django.utils.text import slugify
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Product name')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Url', help_text='You can fill it manually or leave blank for generate automatic')
    description = models.TextField(blank=True, verbose_name='Product description')
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Price')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True, verbose_name='Creation date')
    modified_at = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name='Modified date')

    def get_absolute_url(self):
        return '/product/{}'.format(self.slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if not self.id:
            self.created = datetime.today()

        self.modified = datetime.today()
        return super(Product, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)


class Comment(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True, verbose_name='Comment creation date')

    @property
    def within_24h(self):
        if (datetime.now() - self.created_at) < timedelta(days=1):
            return True
        else:
            return False

    def __unicode__(self):
        try:
            create_time = self.created_at.strftime("%d %B %Y, %H:%M")
        except AttributeError:
            create_time = None
        return 'Comment from {} at {}'.format(self.user.username, create_time)