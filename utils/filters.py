import django_filters
from django.db.models import Q
from apps.posts.models import Post


class PostFilter(django_filters.FilterSet):
    created_from = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_to = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")
    search = django_filters.CharFilter(method="search_filter")

    class Meta:
        model = Post
        fields = ('created_from', 'created_to')

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(author__full_name__icontains=value)
        )