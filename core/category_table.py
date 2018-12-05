from django.urls import reverse

from core.models import Category


class CategoryTable:
    """
    Structures and builds the category table displayed in the header and produces the resulting HTML.
    """

    def __init__(self, rows=8, columns=3):
        self.rows = rows
        self.columns = columns
        self.cells = [[self.Cell() for i in range(self.columns)] for j in range(self.rows)]
        self._fetch_categories()
        self._build_cells()

    ########################
    # == Public methods == #
    ########################

    def render(self):
        """
        Returns the resulting HTML for the table.

        :return: category table HTML
        """
        html = '<table class="dropdown-menu-right dropdown-menu">'
        for row in range(self.rows):
            html += '<tr>'
            for column in range(self.columns):
                html += self.cells[row][column].render()
            html += '</tr>'
        html += '</table>'
        return html

    #########################
    # == Private methods == #
    #########################

    def _fetch_categories(self):
        self.parents = list(Category.objects.filter(parent=None))
        self.children = {}
        for parent in self.parents:
            self.children[parent] = list(Category.objects.filter(parent=parent))

    def _build_cells(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if row % 4 == 0:
                    # insert a row of "header categories" every 4 rows
                    if len(self.parents) == 0:
                        raise self.TableError('ran out of parent categories on row %d, column %d' % (row, column))
                    category = self.parents.pop(0)
                    self.cells[row][column] = self.Cell(category, is_header=True)
                else:
                    # insert the next child of the last "header category" in this column
                    parent = self._header_cell_for(row, column).category
                    children = self.children[parent]
                    if len(children) == 0:
                        raise self.TableError(
                            'ran out of child categories for parent (%s) on row %d, column %d'
                            % (str(parent), row, column)
                        )
                    next_child = children.pop(0)
                    self.cells[row][column] = self.Cell(next_child)

    def _header_cell_for(self, row, column):
        while True:
            cell = self.cells[row][column]
            if cell.is_header:
                return cell
            row -= 1

    ##############
    # == Cell == #
    ##############

    class Cell:

        def __init__(self, category=None, is_header=False):
            self.category = category
            self.is_header = is_header

        def render(self):
            """
            Renders a single cell in the table.

            :return: cell html
            """
            html = '<th class="dropdown_category_text">' if self.is_header else '<td>'
            html += '<a href="' + reverse('category_detail', kwargs={'name': self.category.name}) + '">'
            html += self.category.display_name
            html += '</a>'
            html += '</th>' if self.is_header else '</td>'
            return html

    class TableError(Exception):
        pass


def category_table(request):
    """
    Context processor. Registered in settings.py, this method inserts a CategoryTable into the context of each request.

    :param request: incoming request
    :return: context of category_table
    """
    return {'category_table': CategoryTable()}
