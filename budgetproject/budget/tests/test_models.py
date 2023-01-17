from django.test import TestCase
from budget.models import Project, Expense, Category

class TestModels(TestCase):

    def setUp(self):

        """
        Method for initializing the objects beforehand that can be reused later in test cases.
        """

        self.project1 = Project.objects.create(
            name = 'Budget Management System',
            budget = 5000
        )

        self.category1 = Category.objects.create(
            project = self.project1,
            name = 'Development'
        )

        self.expense1 = Expense.objects.create(
            project = self.project1,
            title = 'Initialization',
            amount = 1000,
            category = self.category1
        )

        self.expense2 = Expense.objects.create(
            project = self.project1,
            title = 'Equipment Purchase',
            amount = 2000,
            category = self.category1
        )

    def test_project_slug_is_assigned_while_creating_project(self):

        """
        Test case to check slugify function works create correct slug.
        """

        self.assertEquals(self.project1.slug, 'budget-management-system')


    def test_budget_left(self):

        """
        Assert that after adding the expenses, amount of expenses is deducted from budget
        and final correct budget is displayed.
        """
        
        self.assertEquals(self.project1.budget_left, 2000)

    def test_project_total_transaction(self):

        """
        Asserts total number of transactions after adding the expenses.
        """

        self.assertEquals(self.project1.total_transactions, 2)