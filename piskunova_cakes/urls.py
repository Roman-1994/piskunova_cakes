
from django.contrib import admin
from django.urls import path, include

from cakes.urls import router
from .yasg import urlpatterns as doc_urls

urlpatterns = [

    path('', include(router.urls)),
    path('', include('cakes.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('auth_vk/', include('rest_framework_social_oauth2.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += doc_urls