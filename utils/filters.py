import django_filters
from apps.posts.models import Post

class PostFilter(django_filters.FilterSet):
    created_from = django_filters.DateFilter(field_name="created_date", lookup_expr="gte")
    created_to = django_filters.DateFilter(field_name="created_date", lookup_expr="lte")

    class Meta:
        model = Post
        fields = ('created_from', 'created_to')