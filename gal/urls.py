from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from core.views import PictureCreate, PictureList, PictureUpdate, PictureDelete

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', PictureList.as_view(template_name='core/gallery.html'), name='gallery'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^picture/create/$', PictureCreate.as_view(), name='picture-create'),
    url(r'^picture/edit/(?P<pk>\d+)/$', PictureUpdate.as_view(), name='picture-edit'),
    url(r'^picture/delete/(?P<pk>\d+)/$', PictureDelete.as_view(), name='picture-delete'),
    url(r'^picture/list/$', PictureList.as_view(), name='picture-list'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
