from rest_framework import routers
from cakes import views
from django.urls import path

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('food/', views.StorageFoodListCreateView.as_view()),
    path('additions/', views.StorageAdditionsListCreateView.as_view()),
    path('desserts/', views.DessertsListView.as_view()),
    path('desserts/<int:pk>/', views.DessertsDetailView.as_view(), name='desserts_detail'),
    path('desserts/<int:pk>/comments/', views.comments),
    path('decors/', views.DecorsListView.as_view()),
    path('decors/<int:pk>/', views.DecorsDetailView.as_view(), name='decors_detail'),
    path('decors/<int:pk>/comments/', views.comments_decor),
    path('orders/', views.OrdersCreateView.as_view()),
    path('ingfood/', views.IngredientsFoodListView.as_view()),
    path('ingadditions/', views.IngredientsAdditionsListView.as_view()),

    path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
]
