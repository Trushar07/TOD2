from budget.forms import ExpenseForm
from django.test import SimpleTestCase

class TestForms(SimpleTestCase):

    def test_expense_form_valid_data(self):

        """
        Assert that with given data, form is valid.
        """

        form = ExpenseForm(data={
            'title' : 'Initialization',
            'amount' : 1000,
            'category' : 'Development'
        })

        self.assertTrue(form.is_valid())


    def test_expense_form_no_data(self):

        """
        Assert that with no data, form is invalid.
        """

        form = ExpenseForm(data={})

        self.assertFalse(form.is_valid())