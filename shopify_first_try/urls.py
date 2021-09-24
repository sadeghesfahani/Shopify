from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings
from django.views.static import serve

urlpatterns = [

    path('admin/', admin.site.urls),
    path('account', include('account.urls')),
    path('', include('store.urls')),
    path('card/', include('card.urls')),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#
# if settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^media/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#     ]
urlpatterns += staticfiles_urlpatterns()