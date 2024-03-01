from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, filters, status, mixins
from api.serializers import QuestionSerializer, ChoiceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from polls.models import Question, Choice
from articles.models import Article
from shop.models import Category, Product, Order, OrderEntry
from . import serializers
from .filters import MinChoiceCountFilter, MaxChoiceCountFilter, MinArticleTextLength, CategoryIdFilter
from .pagination import DefaultPagination


# ____________________________________________________

@api_view(['GET'])
def test_view(request):
    my_param_1 = request.query_params.get('my_param_1')
    my_param_2 = request.query_params.get('my_param_2')
    data = {'status': 'ok', 'param_values': [my_param_1, my_param_2]}
    return Response(data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.prefetch_related('choices')
    serializer_class = QuestionSerializer
    filter_backends = [filters.OrderingFilter]
    pagination_class = DefaultPagination


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = [MinChoiceCountFilter, filters.OrderingFilter, filters.SearchFilter]


# ______________________________

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('id')
    serializer_class = serializers.ArticleSerializer
    pagination_class = DefaultPagination

    filter_backends = [filters.SearchFilter, MinArticleTextLength]
    search_fields = ["id", "title", "authors__first_name", "authors__last_name"]


# ________________________________

class ProductsViewSet(viewsets.mixins.ListModelMixin, viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.prefetch_related('category').order_by('id')
    serializer_class = serializers.ProductSerializer
    pagination_class = DefaultPagination
    filter_backends = [CategoryIdFilter]


class CategoryViewSet(viewsets.mixins.ListModelMixin, viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('id')
    pagination_class = DefaultPagination
    serializer_class = serializers.CategorySerializer


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error: missing param product_id"}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, id=product_id)
        shopping_cart = request.user.profile.shopping_cart
        shopping_cart.order_entries.update_or_create(product=product, defaults={'count': F("count") + 1},
                                                     create_defaults={"product": product, "order": shopping_cart})
        return Response({"detail": 'OK'}, status=status.HTTP_200_OK)


class CartSetView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = serializers.OrderSerializer

    def get(self, request: Request):
        return Response(serializers.OrderSerializer(request.user.profile.shopping_cart).data, status=status.HTTP_200_OK)


class CartUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def update_order_entry(order, update_order_entry: dict):
        order_entry_id = update_order_entry['id']
        order_entry: OrderEntry = order.order_entries.filter(id=order_entry_id).first()
        if order_entry is None:
            return Response(data={'message': f'Unknown order entry id {order_entry_id}'},
                            status=status.HTTP_400_BAD_REQUEST)

        if update_order_entry['remove']:
            order_entry.delete()
        elif update_order_entry['count']:
            order_entry.update(update_order_entry['count'])

    def post(self, request: Request):
        update_order = serializers.OrderSerializer(data=request.data)

        if update_order.is_valid():
            order: Order = request.user.profile.shopping_cart
            update_order_data = update_order.validated_data

            if update_order_data['clear']:
                order.order_entries.all().delete()
            else:
                for update_order_entry_data in update_order_data['order_entries']:
                    self.update_order_entry(order, update_order_entry_data)

            order.save()
            return Response(status=status.HTTP_200_OK)

        return Response(data=update_order.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        shopping_cart = request.user.profile.shopping_cart
        if shopping_cart.order_entries.exists():
            profile = request.user.profile
            shopping_cart.status = Order.Status.COMPLETED
            profile.shopping_cart = Order.objects.create(status=Order.Status.INITIAL, profile=profile)

            shopping_cart.save()
            profile.save()

        return Response(status=status.HTTP_200_OK)


class RepeatOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        shopping_cart = request.user.profile.shopping_cart
        order_id: str = request.data.get('order_id')

        if not order_id or not order_id.isdigit():
            return Response(data={'message': 'Incorrect order id'}, status=status.HTTP_400_BAD_REQUEST)

        order = request.user.profile.orders.filter(id=order_id).first()

        if not order:
            return Response(data={'message': 'Order not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Clear current shopping cart
        shopping_cart.order_entries.all().delete()

        # load order_entries to shoppingcart from selected order
        OrderEntry.objects.bulk_create(
            OrderEntry(count=order_entry.count, product=order_entry.product, order=shopping_cart) for
            order_entry in
            order.order_entries.all())

        return Response(status=status.HTTP_200_OK)


class UserOrders(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    serializer_class = serializers.OrderModelSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(profile=self.request.user.profile)


class UserCreateView(APIView):
    serializers_class = serializers.UserSerializer

    def post(self, request):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, pk: int):
        user = User.objects.get(pk=pk)
        serializer = self.serializers_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        serializer = serializers.UserModelSerializer(request.user)
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = serializers.UserModelSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(data=serializers.UserModelSerializer(request.user).data, status=status.HTTP_200_OK)
