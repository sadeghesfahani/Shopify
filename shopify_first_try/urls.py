from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from product.views import HomeView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('account', include('account.urls')),
    path('', HomeView.as_view(),name='home'),

]

urlpatterns += staticfiles_urlpatterns()