from rest_framework import viewsets, generics
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from cakes.models import *
from cakes.serializers import *
from .service import *

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class UserViewSet(viewsets.ModelViewSet):
    """список пользователей CRUD"""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """список групп CRUD"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class StorageFoodListCreateView(generics.ListCreateAPIView):
    """Вывод списка продуктов"""
    queryset = StorageFood.objects.all()
    serializer_class = StorageFoodSerializer
    #permission_classes = [permissions.IsAdminUser]


class StorageAdditionsListCreateView(generics.ListCreateAPIView):
    """Вывод списка дополнений"""
    queryset = StorageAdditions.objects.all()
    serializer_class = StorageAdditionsSerializer
    #permission_classes = [permissions.IsAdminUser]


class DessertsListView(generics.ListAPIView):
    """Вывод списка десертов"""
    queryset = Desserts.objects.filter(is_active=True)
    serializer_class = DessertsListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DessertsFilter
    #pagination_class = DessertsPagination
    permission_classes = [permissions.AllowAny]


class DessertsDetailView(generics.RetrieveAPIView):
    """Вывод десертa"""
    queryset = Desserts.objects.filter(is_active=True)
    serializer_class = DessertsDetailSerializer
    permission_classes = [permissions.AllowAny]


class IngredientsFoodListView(generics.ListAPIView):
    """Вывод списка ингредиентов продуктов"""
    queryset = IngredientsFood.objects.all()
    serializer_class = IngredientsFoodSerializer
    permission_classes = [permissions.IsAdminUser]


class IngredientsAdditionsListView(generics.ListAPIView):
    """Вывод списка ингредиентов дополнений"""
    queryset = IngredientsAdditions.objects.all()
    serializer_class = IngredientsAdditionsSerializer
    permission_classes = [permissions.IsAdminUser]


class DecorsListView(generics.ListAPIView):
    """Вывод списка декоров"""
    queryset = Decor.objects.filter(is_active=True)
    serializer_class = DecorListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DecorsFilter


class DecorsDetailView(generics.RetrieveAPIView):
    """Вывод декора"""
    queryset = Decor.objects.filter(is_active=True)
    serializer_class = DecorDetailSerializer
    permission_classes = [permissions.AllowAny]


class OrdersCreateView(generics.CreateAPIView):
    """Создание нового заказа"""
    serializer_class = OrdersSerializer


@api_view(['GET', 'POST'])
def comments(request, pk):
    """Вывод и создание комментариев к десерту"""
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = Comment.objects.filter(is_active=True, dessert=pk, parent=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def comments_decor(request, pk):
    """Вывод и создание комментариев к декору"""
    if request.method == 'POST':
        serializer = CommentDecorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = CommentDecor.objects.filter(is_active=True, decor=pk, parent=None)
        serializer = CommentDecorSerializer(comments, many=True)
        return Response(serializer.data)


#class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    #adapter_class = GoogleOAuth2Adapter
    #callback_url = CALLBACK_URL_YOU_SET_ON_GOOGLE
    #client_class = OAuth2Client


class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter


class AddRatingView(APIView):
    """Добаление рейтинга к десерту"""
    def get_client_ip(self, request):
        """Ip адрес автора рейтинга"""
        x_forwarder_for = request.META.get('HTTP_X_FORWARDER_FOR')
        if x_forwarder_for:
            ip = x_forwarder_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_dessert_id(self, request):
        """Id десерта"""
        dessert = request.path
        d = ''
        for i in dessert:
            if i.isdigit():
                d += i
        return Desserts.objects.get(id=int(d))

    def post(self, request, *args, **kwargs):
        serializers = RatingSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(ip=self.get_client_ip(request), dessert=self.get_dessert_id(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ProfitView(viewsets.ViewSet):
    def get(self, request):
        date_start = request.data['date_start']
        date_end = request.data['date_end']
        serializers = ProfitSerializer(data={'date_start': date_start, 'date_end': date_end})
        serializers.is_valid()
        dessert_list = Desserts.objects.filter(created_at__gte=date_start, created_at__lte=date_end)
        profit = []
        for i in dessert_list:
            price_dessert = i.price
            price_food = sum([int(j.price) for j in i.ing_food.all()])
            price_add = sum([int(j.price) for j in i.ing_add.all()])
            if i.decor:
                price_decor_food = 0
                price_decor_add = 0
                if i.decor.ing_food:
                    price_decor_food = int(i.decor.ing_food.price)
                if i.decor.ing_add:
                    price_decor_add = int(i.decor.ing_add.price)
                price_decor = price_decor_food + price_decor_add
            profit.append(price_dessert - price_food - price_add - price_decor)
        return Response(sum(profit))
