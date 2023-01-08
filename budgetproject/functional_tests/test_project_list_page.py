from selenium import webdriver
from budget.models import Project
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
from selenium.webdriver.common.by import By


class TestProjectListPage(StaticLiveServerTestCase):

    def test_foo(self):

        """ Test for first checking whether the webdriver is working or not! """

        self.assertEquals(0,0)

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver')

    def tearDown(self):
        self.browser.close()

    def test_no_projects_alert_is_displayed(self):
        self.browser.get(self.live_server_url)

        """ The user requests the page for the first time. """
        
        alert = self.browser.find_element(By.CLASS_NAME, 'noproject-wrapper')
        self.assertEquals(
            alert.find_element(By.TAG_NAME, 'h3').text,
            'Sorry, you don\'t have any projects, yet.'
        )
    
    def test_no_project_alert_button_redirects_to_add_page(self):

        add_url = self.live_server_url + reverse('add')

        self.browser.get(self.live_server_url)

        """ The user requests the page for the first time. """
        
        alert = self.browser.find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
           self.browser.current_url, add_url
        )

    def test_user_sees_project_list(self):
        project = Project.objects.create(
            name = 'Project 1',
            budget = 4000
        )

        self.browser.get(self.live_server_url)

        """ The User should be able to see project1 on the screen. """

        self.assertEquals(self.browser.find_element(By.TAG_NAME, 'h5').text , 'Project 1')

    
    def test_user_is_redirected_to_project_detail(self):

        project = Project.objects.create(
            name = 'Project 1',
            budget = 4000
        )

        """ The user should see the project detail when he clicks visit"""
        self.browser.get(self.live_server_url)

        detail_url = self.live_server_url + reverse('detail', args = [project.slug])
        
        self.browser.find_element(By.LINK_TEXT, 'VISIT').click()
        self.assertEquals(self.browser.current_url, detail_url)