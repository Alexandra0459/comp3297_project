from django.urls import path
from ASP import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import url, include


urlpatterns =\
[
    path('clinicmanager', views.CMViewsSupply.as_view(), name='clinic-manager'),
    path('clinicmanager/add_order', views.CMViewsSupply.construct_order, name='add-order'),
    path('dispatcher', views.DPViewsOrder.as_view(), name='dispatcher'),
    path('dispatcher/update_order', views.DPViewsOrder.update_order, name='update-order'),
    path('dispatcher/generate_csv', views.DPViewsOrder.get_csv, name='generate_csv'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]

# showing image
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)