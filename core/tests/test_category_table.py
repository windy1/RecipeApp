from django.test import TestCase
from django.utils import timezone

from core.models import Category
from core.category_table import CategoryTable


class CategoryTableTestCase(TestCase):
    """
    A test case for the functionality in core.category_table.CategoryTable
    """

    rows = 8
    columns = 3

    def setUp(self):
        self.categories = [[None for i in range(self.columns)] for j in range(self.rows)]
        for row in range(self.rows):
            for column in range(self.columns):
                self.categories[row][column] = Category.objects.create(
                    created_at=timezone.now(),
                    name=('row_%d_col_%d' % (row, column)),
                    display_name=('Row %d, Column %d' % (row, column)),
                    assignable=True
                )

        for column in range(self.columns):
            parent = self.categories[0][column]
            for row in range(1, 4):
                self.categories[row][column].parent = parent
                self.categories[row][column].save()

        for column in range(self.columns):
            parent = self.categories[4][column]
            for row in range(5, 8):
                self.categories[row][column].parent = parent
                self.categories[row][column].save()

    def test_category_table(self):
        categories = self.categories
        print(categories)
        html = CategoryTable().render()
        print(html)
