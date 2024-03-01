from django.db.models import QuerySet, Count
from django.db.models.functions import Length
from rest_framework import filters
from rest_framework.request import Request

from api.serializers import CategorySerializer


class MinChoiceCountFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        min_choice_count = request.query_params.get("min_choice_count")
        if min_choice_count:
            queryset = queryset.annotate(choice_count=Count('choices')).filter(choice_count__gte=min_choice_count)
        return queryset


class MaxChoiceCountFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        max_choice_count = request.query_params.get("max_choice_count")
        if max_choice_count:
            queryset = queryset.annotate(choice_count=Count('choices')).filter(choice_count__lte=max_choice_count)
        return queryset


class MinArticleTextLength(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_article_text_length = request.query_params.get("min_article_text_length")
        if min_article_text_length:
            queryset = queryset.annotate(text_length=Length('text')).filter(text_length__gt=min_article_text_length)
        return queryset


class CategoryIdFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        category_id = request.query_params.get("category_id")
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset


class IncludeProductsFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        include_products = request.query_params.get("include_products")
        if include_products:
            view.serializer_class = CategoriesSerializer
        return queryset
