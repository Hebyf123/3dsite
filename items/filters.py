import django_filters
from django.utils.translation import gettext as _
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', field_name='name', label=_('Название продукта'))
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label=_('Категория'))
    price_min = django_filters.NumberFilter(field_name='min_price', lookup_expr='gte', label=_('Минимальная цена от'), required=False)
    price_max = django_filters.NumberFilter(field_name='max_price', lookup_expr='lte', label=_('Максимальная цена до'), required=False)

    class Meta:
        model = Product
        fields = ['name', 'category', 'price_min', 'price_max']
