# tests.py (support)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov

"""
This file houses test cases for the Support module.

Available functions:
- None
"""

# TODO Test Email sender:
# https://stackoverflow.com/questions/3728528/testing-email-sending.

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.test.client import RequestFactory
from support.test_data.support_data import SUPPORT_ONE, data, files, SUPPORT_FORM


class TestSupport(TestCase):
    """Test the functions related to Support module."""

    def setUp(self):
        """Prepare necessary objects for testing the Support module."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.factory = RequestFactory()

    def test_home(self):
        """Tests the home page."""
        # Response = self.client.get('/support/index').
        response = self.client.get('/support/index/')
        self.assertContains(response, 'Help/Suggestions', 0, 200)

    def test_request_information_view_get(self):
        """Tests the Request Information View get page."""
        response = self.client.get('/support/request_info/', SUPPORT_ONE)
        self.assertContains(response, 'information', 3, 200)

    def test_request_information_view_post(self):
        """Tests the Request Information View post page."""
        response = self.client.post('/support/request_info/', SUPPORT_ONE)
        self.assertContains(response, 'information', 1, 200)

    def test_user_manual_view_get(self):
        """Tests the User Manual View get page."""
        response = self.client.get('/support/manual/', SUPPORT_ONE)
        self.assertContains(response, 'manual', 5, 200)

    def test_user_create_get(self):
        """Tests the create get page."""
        response = self.client.get('/support/create/', data, files)
        print(response)
        self.assertContains(response, 'create', 2, 200)

    def test_user_create_post(self):
        """Tests the create post page."""
        response = self.client.post('/support/create/', data)
        print(response)
        self.assertContains(response, 'create', 2, 200)

    def test_list_supports_get(self):
        """Tests the list supports get."""
        response = self.client.get('/support/list/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_list_supports_post(self):
        """Tests the list supports post."""
        response = self.client.post('/support/list/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_search_support_get(self):
        """Tests the search support get."""
        response = self.client.get('/support/search/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_search_support_post(self):
        """Tests the search support post."""
        response = self.client.post('/support/search/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_search_support_for_last_30_get(self):
        """Tests the search support for last30 get."""
        response = self.client.get('/support/support/search/result/thirty/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_search_support_for_last_30_post(self):
        """Tests the search support for last30 post."""
        response = self.client.post('/support/support/search/result/thirty/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_search_support_for_last_60_get(self):
        """Tests the search support for last60 get."""
        response = self.client.get('/support/support/search/result/sixty/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_search_support_for_last_60_post(self):
        """Tests the search support for last60 post."""
        response = self.client.post('/support/support/search/result/sixty/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_search_support_for_last_90_get(self):
        """Tests the search support for last90 get."""
        response = self.client.get('/support/support/search/result/ninety/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_search_support_for_last_90_post(self):
        """Tests the search support for last90 post."""
        response = self.client.post('/support/support/search/result/ninety/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_search_support_for_last_180_get(self):
        """Tests the search support for last180 get."""
        response = self.client.get('/support/support/search/result/one_eighty/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_search_support_for_last_180_post(self):
        """Tests the search support for last180 post."""
        response = self.client.post('/support/support/search/result/one_eighty/', SUPPORT_FORM)
        self.assertContains(response, 'id', 25, 200)

    def test_create_support_type_get(self):
        """Tests the create support type get."""
        response = self.client.get('/support/type/create/', SUPPORT_FORM)
        self.assertContains(response, 'id', 30, 200)

    def test_create_support_type_post(self):
        """Tests the create support type post."""
        response = self.client.post('/support/type/create/', SUPPORT_FORM)
        self.assertContains(response, 'id', 0, 302)

    def test_create_priority_post(self):
        """Tests the create priority post."""
        response = self.client.post('/support/priority/create/', SUPPORT_FORM)
        self.assertContains(response, 'id', 0, 302)
