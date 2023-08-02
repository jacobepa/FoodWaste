# test_views.py (DataSearch)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=W0511,R0904
"""
This file demonstrates writing tests using the unittest module.

These will pass when you run "manage.py test".
"""

# from unittest import TestCase
import django
from django.contrib.auth.models import User, Permission
from django.db.models.query import QuerySet, EmptyQuerySet
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from DataSearch.forms import ExistingDataForm
from DataSearch.models import Attachment, ExistingData, ExistingDataSource, \
    ExistingDataSharingTeamMap
from DataSearch.views import get_existing_data_all, check_can_edit, \
    get_existing_data_team, get_existing_data_user, ExistingDataDetail, \
    ExistingDataEdit, existing_form_process_teams_attachments
from teams.models import Team, TeamMembership


class TestViewAuthenticated(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS.
        @classmethod
        def setUpClass(cls):
            """Prepare objects for testing."""
            super(TestViewAuthenticated, cls).setUpClass()
            django.setup()

    def setUp(self):
        """Prepare various objects for this class of tests."""
        self.request_factory = RequestFactory()
        self.test_str = 'Test'
        self.client = Client()
        # User 1 created the team, User 2 created ExistingData,
        # User 3 has no privileges
        self.user1 = User.objects.create_user(username='testuser',
                                              password='12345', is_staff=True)
        self.client.login(username='testuser', password='12345')


        self.user2 = User.objects.create_user(username='testuser2',
                                              password='12345')
        self.user3 = User.objects.create_user(username='testuser3',
                                              password='12345')
        self.user4 = User.objects.create_user(username='testuser4',
                                              password='12345', is_staff=True,
                                              is_superuser=True)

        # Assuming the URL name for the protected_view is 'protected_view'
        self.client.login(username='testuser', password='12345')
        # self.user = User.objects.get(id=1)
        self.team = Team.objects.create(created_by=self.user1, name='testteam')
        TeamMembership.objects.create(member=self.user1,
                                      team=self.team,
                                      is_owner=True,
                                      can_edit=True)
        # Build some models to be used in this test class:
        self.source = ExistingDataSource.objects.get(id=1)
        self.data_dict = {
          'work': self.test_str,
          'email': self.test_str,
          'phone': self.test_str,
          'search': self.test_str,
          'source': self.source,
          'source_title': self.test_str,
          'keywords': self.test_str,
          'url': self.test_str,
          'disclaimer_req': True,
          'citation': self.test_str,
          'comments': self.test_str,
          'created_by': self.user2,
          'teams': []
        }
        self.dat = ExistingData.objects.create(work=self.test_str,
                                               email=self.test_str,
                                               phone=self.test_str,
                                               search=self.test_str,
                                               source=self.source,
                                               source_title=self.test_str,
                                               keywords=self.test_str,
                                               url=self.test_str,
                                               disclaimer_req=False,
                                               citation=self.test_str,
                                               comments=self.test_str,
                                               created_by=self.user2)
        self.dat_team_map = ExistingDataSharingTeamMap.objects.create(
          data=self.dat, team=self.team, can_edit=True)
        self.dat.teams.add(self.dat_team_map.team)
        self.file = SimpleUploadedFile('test.txt', b'This is a test file.')
        # TODO: Need at least one QAPP and SectionA object to
        # fully test clean_qapps

    def test_home(self):
        """Tests loading the home page."""
        response = self.client.get('/')
        self.assertContains(response,
                            'Existing Data and Information Search Tool', 1,
                            200)
        self.assertContains(response, 'QAPP Development',
                            1, 200)

    def test_contact(self):
        """Tests loading the contact page."""
        response = self.client.get('/contact')
        self.assertContains(response,
                            'EDAB | Environmental Decision Analytics Branch.',
                            1, 200)
        self.assertContains(response, 'Plastics Projects Research (EDAB)', 1,
                            200)

    def test_web_dev_tools_get(self):
        """Tests loading the dev tools page."""
        response = self.client.get('/dev')
        self.assertContains(response, 'QAPP Module Management', 1, 200)
        self.assertContains(response, 'Clean and Convert QAPP Data', 1,
                            200)

    def test_clean_qapps(self):
        """Test the clean qapps function."""
        response = self.client.get('/dev/clean_qapps')
        self.assertContains(response, 'QAPP Module Management', 1, 200)
        self.assertContains(response, 'Clean and Convert QAPP Data', 1,
                            200)

    def test_get_existing_data_all(self):
        """Test the function to return all existing data objects."""
        data = get_existing_data_all()
        self.assertIsInstance(data, QuerySet)
        self.assertNotIsInstance(data, EmptyQuerySet)
        self.assertEqual(len(data), 1)

    def test_get_existing_data_user(self):
        """Test the function to return all existing data for a given user."""
        data = get_existing_data_user(self.user2.id)
        self.assertIsInstance(data, QuerySet)
        self.assertNotIsInstance(data, EmptyQuerySet)
        self.assertEqual(len(data), 1)

    def test_get_existing_data_team(self):
        """Test the function to return all existing data for a given team."""
        data = get_existing_data_team(self.team.id)
        self.assertIsInstance(data, QuerySet)
        self.assertNotIsInstance(data, EmptyQuerySet)
        self.assertEqual(len(data), 1)

    def test_get_existing_data_team_empty(self):
        """
        Test the function to return all existing data for a given team that
        doesn't exist. This should return an empty queryset.
        """
        data = get_existing_data_team(0)
        self.assertNotIsInstance(data, QuerySet)
        self.assertEqual(len(data), 0)

    def test_check_can_edit_user(self):
        """
        Test the function that checks if a user has user-level
        permissions to edit the given Existing Data.
        """
        self.assertTrue(check_can_edit(self.dat, self.user2))

    def test_check_can_edit_team(self):
        """
        Test the function that checks if a user has team-level
        permissions to edit the given Existing Data.
        """
        self.assertTrue(check_can_edit(self.dat, self.user1))

    def test_check_can_edit_super(self):
        """
        Test the function that checks if a user has super
        permissions to edit the given Existing Data.
        """
        self.assertTrue(check_can_edit(self.dat, self.user4))

    def test_check_can_edit_fail(self):
        """
        Test the user permission check function against
        a user with no permissions.
        """
        self.assertFalse(check_can_edit(self.dat, self.user3))

    def test_existingdata_index(self):
        """Test loading the Existing Data index page."""
        response = self.client.get('/existingdata')
        self.assertContains(response, 'Existing Data Tracking Tool', 1, 200)
        self.assertContains(response,
                            'Existing Data and Information Research Projects',
                            1, 200)
        self.assertContains(response, 'View existing entries by', 2, 200)
        self.assertContains(response, 'New Team', 1, 200)
        self.assertContains(response, 'New Existing Data', 1, 200)

    def test_existingdata_list_user(self):
        """Test loading the list of Existing Data for a specified user."""
        response = self.client.get('/existingdata/list/user/' +
                                   str(self.user1.id))
        self.assertContains(response, 'Existing Data Tracking Tool', 1, 200)
        self.assertContains(response, 'View or Edit Existing Data', 1, 200)
        self.assertContains(response, 'Export All Data to Docx', 1, 200)
        self.assertContains(response, 'Export All Data to PDF', 1, 200)
        self.assertContains(response, 'Export All Data to Excel', 1, 200)

    def test_existingdata_list_team(self):
        """Test loading the list of Existing Data for a specified team."""
        response = self.client.get('/existingdata/list/team/' +
                                   str(self.team.id))
        self.assertContains(response, 'Existing Data Tracking Tool', 1, 200)
        self.assertContains(response, 'View or Edit Existing Data', 1, 200)
        self.assertContains(response, 'Export All Data to Docx', 1, 200)
        self.assertContains(response, 'Export All Data to PDF', 1, 200)
        self.assertContains(response, 'Export All Data to Excel', 1, 200)

    def test_existingdata_list_all(self):
        """Test loading the list of all Existing Data."""
        response = self.client.get('/existingdata/list/')
        self.assertContains(response, 'Existing Data Tracking Tool', 1, 200)
        self.assertContains(response, 'View or Edit Existing Data', 1, 200)
        self.assertContains(response, 'Export All Data to Docx', 1, 200)
        self.assertContains(response, 'Export All Data to PDF', 1, 200)
        self.assertContains(response, 'Export All Data to Excel', 1, 200)

    def test_existingdata_detail_team(self):
        """
        Test loading details page for a specified existing data object,
        called from the team list page.
        """
        header = {
          'HTTP_REFERER': '/existingdata/list/team/' + str(self.team.id)
        }
        response = self.client.get('/existingdata/detail/' + str(self.dat.id),
                                   **header)
        self.assertContains(response, 'Details for Existing Data', 1, 200)
        self.assertContains(response, 'Export to Docx', 1, 200)
        self.assertContains(response, 'Export to PDF', 1, 200)
        self.assertContains(response, 'Export to Excel', 1, 200)
        self.assertContains(response, 'Back', 1, 200)
        self.assertContains(response, 'Edit Data Entry', 1, 200)
        self.assertContains(response, 'Delete Data Entry', 1, 200)

    def test_existingdata_detail_user(self):
        """
        Test loading details page for a specified existing data object,
        called from the user list page.
        """
        header = {
          'HTTP_REFERER': '/existingdata/list/user/' + str(self.user1.id)
        }
        response = self.client.get('/existingdata/detail/' + str(self.dat.id),
                                   **header)
        self.assertContains(response, 'Details for Existing Data', 1, 200)
        self.assertContains(response, 'Export to Docx', 1, 200)
        self.assertContains(response, 'Export to PDF', 1, 200)
        self.assertContains(response, 'Export to Excel', 1, 200)
        self.assertContains(response, 'Back', 1, 200)
        self.assertContains(response, 'Edit Data Entry', 1, 200)
        self.assertContains(response, 'Delete Data Entry', 1, 200)

    def test_existingdata_detail_no_edit(self):
        """
        Test loading details page for a specified existing data object
        where the requesting user doesn't have edit permissions.
        """
        header = {
          'HTTP_REFERER': '/existingdata/list/user/' + str(self.user1.id)
        }
        path = '/existingdata/detail/' + str(self.dat.id)
        request = self.request_factory.get(path, **header)
        request.user = self.user3
        response = ExistingDataDetail.as_view()(pk=str(self.dat.id),
                                                request=request)
        self.assertContains(response, 'Details for Existing Data', 1, 200)
        self.assertContains(response, 'Export to Docx', 1, 200)
        self.assertContains(response, 'Export to PDF', 1, 200)
        self.assertContains(response, 'Export to Excel', 1, 200)
        self.assertContains(response, 'Back', 1, 200)
        self.assertNotContains(response, 'Edit Data Entry', 200)
        self.assertNotContains(response, 'Delete Data Entry', 200)
        self.assertContains(response, 'You cannot edit this data', 1, 200)

    def test_existingdata_edit_get(self):
        """Test loading edit page for a specified existing data object."""
        response = self.client.get('/existingdata/edit/' + str(self.dat.id))
        self.assertContains(response, 'Save', 1, 200)
        self.assertContains(response, 'Reset', 1, 200)
        self.assertContains(response, 'Cancel', 1, 200)

    def test_existingdata_edit_get_no(self):
        """
        Test loading edit page for a specified existing data object when
        the requesting user has no permissions to edit.
        """
        request = self.request_factory.get('/existingdata/edit/' +
                                           str(self.dat.id))
        request.user = self.user3
        response = ExistingDataEdit.as_view()(pk=str(self.dat.id),
                                              request=request)
        self.assertEqual(response.status_code, 302)

    def test_existingdata_edit_post(self):
        """Test editing an existingdata object via POST."""
        path = '/existingdata/edit/' + str(self.dat.id)
        response = self.client.post(path, data=self.data_dict)
        self.assertEqual(response.status_code, 200)

    def test_existingdata_edit_post_no(self):
        """
        Test editing an existingdata object via POST when
        the requesting user has no permissions to edit.
        """
        path = '/existingdata/edit/' + str(self.dat.id)
        request = self.request_factory.post(path, data=self.data_dict)
        request.user = self.user3
        response = ExistingDataEdit.as_view()(pk=str(self.dat.id),
                                              request=request)
        self.assertEqual(response.status_code, 302)

    def test_existing_form_process_teams_attachments(self):
        """
        Test the function that processes a new Existing Data form's multiple
        attachments and teams.
        """
        data_dict = self.data_dict
        # Set a new team
        team = Team.objects.create(created_by=self.user1, name='testteam2')
        TeamMembership.objects.create(member=self.user1,
                                      team=team,
                                      is_owner=True,
                                      can_edit=True)
        data_dict['teams'].append(team.id)
        form = ExistingDataForm(self.data_dict,
                                user=self.user1,
                                instance=self.dat)
        clean = form.is_valid()
        self.assertTrue(clean)

        path = '/existingdata/edit/' + str(self.dat.id)
        request = self.request_factory.post(path, data=self.data_dict)
        request.user = self.user2
        # Set up some attachments
        request.FILES['file'] = self.file

        response = existing_form_process_teams_attachments(request,
                                                           form,
                                                           instance=self.dat)
        self.assertTrue(isinstance(response, ExistingData))

    def test_existingdata_create_get(self):
        """Test loading the Existing Data Create page."""
        response = self.client.get('/existingdata/create/')
        self.assertContains(response, 'Save', 1, 200)
        self.assertContains(response, 'Reset', 1, 200)
        self.assertContains(response, 'Cancel', 1, 200)

    def test_existingdata_create_post(self):
        """
        Test Create ExistingData with a valid form.
        This should redirect to the new object's detail page.
        """
        data = self.data_dict
        data['source'] = 1
        response = self.client.post('/existingdata/create/', data=data)
        self.assertEqual(response.status_code, 302)

    def test_existingdata_create_post_2(self):
        """
        Test Create ExistingData with a non-valid form.
        This should render the create page again.
        """
        response = self.client.post('/existingdata/create/', data={})
        self.assertContains(response, 'Save', 1, 200)
        self.assertContains(response, 'Reset', 1, 200)
        self.assertContains(response, 'Cancel', 1, 200)

    def test_existing_data_delete(self):
        """Test Delete ExistingData with a valid PK"""
        obj = ExistingData.objects.create(work=self.test_str,
                                          email=self.test_str,
                                          phone=self.test_str,
                                          search=self.test_str,
                                          source=self.source,
                                          source_title=self.test_str,
                                          keywords=self.test_str,
                                          url=self.test_str,
                                          disclaimer_req=False,
                                          citation=self.test_str,
                                          comments=self.test_str,
                                          created_by=self.user2)
        response = self.client.post(f'/existingdata/delete/{obj.id}')
        self.assertEqual(response.status_code, 302)

    def test_existing_data_delete_2(self):
        """Test Delete ExistingData with a non-valid PK"""
        response = self.client.post('/existingdata/delete/x')
        self.assertEqual(response.status_code, 404)

    def test_attachments_download_1(self):
        """Test attachments download function, download all attachments."""
        att1 = Attachment.objects.create(name='Test1',
                                         file=self.file,
                                         uploaded_by=self.user1)
        att2 = Attachment.objects.create(name='Test2',
                                         file=self.file,
                                         uploaded_by=self.user1)
        self.dat.attachments.add(att1)
        self.dat.attachments.add(att2)
        path = f'/existingdata/download_attachments/{self.dat.id}/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'This is a test file' in response.content)

    def test_attachments_download_2(self):
        """Test attachments download function, download one attachment."""
        att = Attachment.objects.create(name='Test3',
                                        file=self.file,
                                        uploaded_by=self.user1)
        self.dat.attachments.add(att)
        path = f'/existingdata/download_attachment/{self.dat.id}/{att.id}/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'This is a test file' in response.content)

    def test_attachment_delete(self):
        """
        Test attachment delete function.
        Function redirects to Details page.
        """
        att = Attachment.objects.create(name='Test',
                                        file=self.file,
                                        uploaded_by=self.user1)
        self.dat.attachments.add(att)
        path = f'/existingdata/delete_attachment/{self.dat.id}/{att.id}/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
