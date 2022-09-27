from rest_framework import routers
from cakes import views
from django.urls import path

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'food', views.StorageFoodViewSet)
router.register(r'additions', views.StorageAdditionsViewSet)
router.register(r'desserts', views.DessertsViewSet)
router.register(r'ingfood', views.IngredientsFoodViewSet)

urlpatterns = [

]
