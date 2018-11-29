from django.shortcuts import render, get_object_or_404

from core.models import Category


def categories(request):
    """
    Displays all root-level categories available for browsing.
    """
    category_list = Category.objects.filter(parent=None)
    context = {'category_list': category_list, 'explore': 'categories'}
    return render(request, 'core/categories/category_list.html', context)


def category_detail(request, name):
    """
    Displays a selected categories, as specified by the URL. If the categories has sub-categories, those will be
    displayed instead of recipes in that categories.
    """
    category = get_object_or_404(Category, name=name)
    sub_categories = Category.objects.filter(parent=category).order_by('-name')
    context = {'categories': category, 'explore': 'categories'}

    if sub_categories.count() > 0:
        # if the categories has no sub-categories, list out the recipes in that categories
        context['category_list'] = sub_categories
        return render(request, 'core/categories/category_list.html', context)

    # list the categories's sub-categories
    context['recipe_list'] = sorted(category.recipe_set.all(), key=lambda r: r.avg_rating(), reverse=True)
    return render(request, 'core/categories/category_detail.html', context)
