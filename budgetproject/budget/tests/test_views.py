from django.test import TestCase, Client
from django.urls import reverse
from budget.models import Project, Category, Expense
import json

class TestViews(TestCase):

    def setUp(self):

        """
        Method for initializing the objects beforehand that can be reused later in test cases.
        """
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args = ['project1'])

        self.project1 = Project.objects.create(
            name = 'project1',
            budget = 100
        )

        self.category1 = Category.objects.create(
            project = self.project1,
            name = 'start up'
        )


    def test_project_list_GET(self):

        """
        Assert that the template with the provided name was used in rendering the response
        """

        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, 'budget/project-list.html')


    def test_project_detail_GET(self):

        """
        Assert that the template with the provided name was used in rendering the response
        """

        response = self.client.get(self.detail_url)

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, 'budget/project-detail.html')

    
    def test_project_detail_POST_adds_new_expense(self):

        """ 
        To check whether new expense is added or not, we would check the title of the
        latest expense.
        """

        response = self.client.post(self.detail_url, {
            'title' : 'expense1',
            'amount' : 10,
            'category' : self.category1

        })

        self.assertEquals(response.status_code, 302)

        self.assertEquals(self.project1.expenses.first().title, 'expense1')


    def test_project_detail_POST_no_data(self):

        """ 
        Test to check post request to add expense without data should not
        add new expense
        """

        response = self.client.post(self.detail_url) # POST request without data

        self.assertEquals(response.status_code, 302)

        self.assertEquals(self.project1.expenses.count(), 0)


    def test_project_detail_DELETE_deletes_expense(self):

        """
        Assert that the given expense is deleted from database and expense is removed
        from budget.
        """

        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 10,
            category = self.category1
        )

        response = self.client.delete(self.detail_url, json.dumps({
            'id' : 1
        }))

        self.assertEquals(response.status_code, 204)
        self.assertEquals(self.project1.expenses.count(), 0)


    def test_project_detail_DELETE_no_data(self):

        """
        Assert that delete request without data(id) should not delete expense and
        number of transactions remains same.
        """

        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 10,
            category = self.category1
        )

        response = self.client.delete(self.detail_url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(self.project1.expenses.count(), 1)


    def test_project_create_POST(self):

        """
        Test case to create new project.
        """
        url = reverse('add')

        response = self.client.post(url, {
            'name' : 'project2',
            'budget': 1000,
            'categoriesString' : 'StartUp,Equipment'
        })

        """
        Assert that above post request adds new project bject.
        """
        project2 = Project.objects.get(id=2)
        self.assertEquals(project2.name, 'project2')
        self.assertEquals(Project.objects.all().count(), 2)

        """
        Assert that above post request adds first category object.
        """

        first_category = Category.objects.get(id=2)
        self.assertEquals(first_category.project, project2)
        self.assertEquals(first_category.name, 'StartUp')

        """
        Assert that above post request adds second category object.
        """

        second_category = Category.objects.get(id=3)
        self.assertEquals(second_category.project, project2)
        self.assertEquals(second_category.name, 'Equipment')