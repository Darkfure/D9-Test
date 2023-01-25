from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category
from django import forms


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='без фильтрации'
    )
    create_time = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                      lookup_expr='gt',
                      label='Date')

    class Meta:
        model = Post
        fields = ['heading', 'category', 'create_time']

