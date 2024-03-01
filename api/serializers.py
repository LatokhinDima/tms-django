from rest_framework import serializers
from polls.models import Question, Choice
from django.contrib.auth.models import User
from articles.models import Article
from rest_framework import serializers
from shop.models import Category, Product, OrderEntry, Order


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


# __________________________________
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


# ___________________________________
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        include_products = self.context['request'].query_params.get('include_products', 'true')
        if include_products == 'false' and 'products' in self.fields:
            self.fields.pop('products')
        return super().to_representation(instance)

    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"


class UpdateOrderEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    remove = serializers.BooleanField(required=False, default=False)
    count = serializers.IntegerField(required=False, default=None, allow_null=True)


class OrderSerializer(serializers.Serializer):
    clear = serializers.BooleanField(required=False, default=False)
    order_entries = UpdateOrderEntrySerializer(many=True, required=False, default=[])


class OrderEntryModelSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderEntry
        fields = '__all__'


class OrderModelSerializer(serializers.ModelSerializer):
    order_entries = OrderEntryModelSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def create(self, validated_data: dict) -> User:
        if validated_data["password"] != validated_data["password2"]:
            raise serializers.ValidationError({"password": "Password do not match"})

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )

        user.set_password(validated_data["password"])
        user.save()

        return user

    def update(self, instance: User, validated_data: dict) -> User:
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)

        if validated_data.get("password"):
            instance.set_password(validated_data["password"])

        instance.save()

        return instance
