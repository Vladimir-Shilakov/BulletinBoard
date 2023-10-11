from django_filters import FilterSet
from .models import Ads


class AdsFilter(FilterSet):
    class Meta:
        model = Ads
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'time_created': ['date__gte']
            }
