from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart

User = get_user_model()


class IngredientFilter(SearchFilter):
    """фильтр поиска ингридиентов."""
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    """Фильтр поиска рецептов."""
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='if_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='if_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        if self.request.user.is_authenticated:
            is_favorited = Favorite.objects.filter(
                user=self.request.user,
                recipe=OuterRef('id')
            )
            is_in_shopping_cart = ShoppingCart.objects.filter(
                user=self.request.user,
                recipe=OuterRef('id')
            )
            queryset = queryset.annotate(
                is_favorited=Exists(is_favorited),
                is_in_shopping_cart=Exists(is_in_shopping_cart)
            )

        return queryset

    def if_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(
                favorites__user=self.request.user
            )
        return queryset

    def if_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(
                shopping_list__user=self.request.user
            )
        return queryset
