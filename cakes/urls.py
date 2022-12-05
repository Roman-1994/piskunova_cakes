from rest_framework import routers
from cakes import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('food/', views.StorageFoodListCreateView.as_view(), name='food'),
    path('additions/', views.StorageAdditionsListCreateView.as_view(), name='additions'),
    path('desserts/', views.DessertsListView.as_view(), name='desserts_list'),
    path('desserts/<int:pk>/', views.DessertsDetailView.as_view(), name='desserts_detail'),
    path('desserts/<int:pk>/comments/', views.comments),
    path('desserts/<int:pk>/comments/rating/', views.AddRatingView.as_view()),
    path('decors/', views.DecorsListView.as_view()),
    path('decors/<int:pk>/', views.DecorsDetailView.as_view(), name='decors_detail'),
    path('decors/<int:pk>/comments/', views.comments_decor),
    path('orders/', views.OrdersCreateView.as_view()),
    path('ingfood/', views.IngredientsFoodListView.as_view(), name='ingfood'),
    path('ingadditions/', views.IngredientsAdditionsListView.as_view()),
    path('profit/', views.ProfitView.as_view({'get': 'get'})),

    path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

