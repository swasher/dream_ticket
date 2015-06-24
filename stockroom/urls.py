from django.conf.urls import patterns, url
from .views import grid, about, product, set_like

urlpatterns = patterns('',
    url(r'^$', grid),
    url(r'^grid/$', grid, name='grid'),
    url(r'^product/(?P<slug>[-\w]+)/$', product, name='product'),
    url(r'^set_like/(?P<id>\d+)/$', set_like, name='set_like'),
    # TODO deprecated url(r'^add_comment/$', add_comment, name='add_comment'),
    url(r'^about/$', about, name='about'),
)

