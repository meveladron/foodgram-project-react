from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.paginator import CustomPaginator
from api.permissions import (IsAdminOrReadOnly, IsAuthorOrReadOnly,
                             IsModeratorOrReadOnly)
from api.serializers import (CreateRecipeSerializer, FavoriteSerializer,
                             IngredientSerializer, ShoppingCartSerializer,
                             ShowRecipeSerializer, TagSerializer)
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [IngredientFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = CreateRecipeSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly | IsModeratorOrReadOnly | IsAdminOrReadOnly
    ]
    pagination_class = CustomPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.all()
        if not user.is_anonymous:
            is_favorited = Favorite.objects.filter(
                user=user,
                recipe=OuterRef('id')
            )
            is_in_shopping_cart = ShoppingCart.objects.filter(
                user=user,
                recipe=OuterRef('id')
            )
            queryset = Recipe.objects.prefetch_related('ingredients').annotate(
                is_favorited=Exists(is_favorited),
                is_in_shopping_cart=Exists(is_in_shopping_cart)
            )
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRecipeSerializer
        else:
            return CreateRecipeSerializer

    @action(
        detail=False, methods=["GET"], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        final_list = {}
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_list__user=request.user
        ).values_list(
            "ingredient__name", "ingredient__measurement_unit", "amount"
        )
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    "measurement_unit": item[1],
                    "amount": item[2],
                }
            else:
                final_list[name]["amount"] += item[2]
        pdfmetrics.registerFont(
            TTFont("caviar-dreams", "data/TimesNewRoman.ttf", "UTF-8")
        )
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            "attachment; filename='shopping_list.pdf'"
        )
        page = canvas.Canvas(response)
        page.setFont("caviar-dreams", size=16)
        page.drawString(200, 800, "Список покупок для приготовления рецепта")
        page.setFont("caviar-dreams", size=14)
        height = 700
        for i, (name, data) in enumerate(final_list.items(), 1):
            page.drawString(
                75, height, (
                    f'{i}. {name} - {data["amount"]} '
                    f'{data["measurement_unit"]}'
                ),
            )
            height -= 25
        page.showPage()
        page.save()
        return response


class FavoritesShoppingCartBasicViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'recipe': kwargs.get('id')
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        favorite = kwargs.get('id')
        self.model.objects.filter(
            user=request.user.id,
            recipe=favorite
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(FavoritesShoppingCartBasicViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    model = Favorite


class ShoppingCartViewSet(FavoritesShoppingCartBasicViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    model = ShoppingCart
