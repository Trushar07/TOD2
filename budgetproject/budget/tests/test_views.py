from django.test import TestCase, Client
from django.urls import reverse
from budget.models import Project, Category, Expense
import json

class TestViews(TestCase):

    def setUp(self):
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

        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code, 200)

        """
        Assert that the template with the provided name was used in rendering the response
        """
        self.assertTemplateUsed(response, 'budget/project-list.html')


    def test_project_detail_GET(self):

        response = self.client.get(self.detail_url)

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, 'budget/project-detail.html')

    
    def test_project_detail_POST_adds_new_expense(self):

        response = self.client.post(self.detail_url, {
            'title' : 'expense1',
            'amount' : 10,
            'category' : self.category1

        })

        self.assertEquals(response.status_code, 302)

        """ To check whether new expense is added or not, we would check the title of the
        latest expense"""

        self.assertEquals(self.project1.expenses.first().title, 'expense1')


    def test_project_detail_POST_no_data(self):

        """ Test to check post request to add expense without data should not
        add new expense"""

        response = self.client.post(self.detail_url) # POST request without data

        self.assertEquals(response.status_code, 302)

        self.assertEquals(self.project1.expenses.count(), 0)


    def test_project_detail_DELETE_deletes_expense(self):
        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 10,
            category = self.category1
        )