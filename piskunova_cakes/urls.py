
from django.contrib import admin
from django.urls import path, include

from cakes.urls import router

urlpatterns = [

    path('', include(router.urls)),
    path('api/', include('cakes.urls')),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
