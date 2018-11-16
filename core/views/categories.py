from django.shortcuts import render, get_object_or_404

from core.models import Category


def categories(request):
    category_list = Category.objects.filter(parent=None)
    context = {'category_list': category_list, 'explore': 'category'}
    return render(request, 'core/category/category_list.html', context)


def category_detail(request, name):
    category = get_object_or_404(Category, name=name)
    sub_categories = Category.objects.filter(parent=category).order_by('-name')
    context = {'category': category, 'explore': 'category'}

    if sub_categories.count() > 0:
        # if the category has no sub-categories, list out the recipes in that category
        context['category_list'] = sub_categories
        return render(request, 'core/category/category_list.html', context)

    # list the category's sub-categories
    context['recipe_list'] = category.recipe_set.order_by('-avg_rating')
    return render(request, 'core/category/category_detail.html', context)
