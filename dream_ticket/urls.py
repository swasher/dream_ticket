from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('stockroom.urls')),

    #url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS

    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^login/$', 'stockroom.views.login', name='login'),
    url(r'^logout/$', 'stockroom.views.logout', name='logout'),
    url(r'^login_redirect/$', 'stockroom.views.login_redirect', name='login_redirect'),

)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

