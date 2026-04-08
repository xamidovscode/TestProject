import django_filters
from apps.posts.models import Post

class PostFilter(django_filters.FilterSet):
    author__full_name = django_filters.CharFilter(field_name='author__full_name', lookup_expr='istartswith')
    title = django_filters.CharFilter(field_name='title', lookup_expr='istartswith')
    created_from = django_filters.DateFilter(field_name="created_date", lookup_expr="gte")
    created_to = django_filters.DateFilter(field_name="created_date", lookup_expr="lte")

    class Meta:
        model = Post
        fields = ('author__full_name', 'title', 'created_from', 'created_to')