from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task
from django.utils import timezone


class TaskAPITestCase(APITestCase):
    """
    Test cases for task-related API endpoints.
    
    This test case covers creating tasks via the Task Management API.
    In future it will be expanded to test reading, updating, and deleting tasks.
    """

    # Set up data for the tests
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            due_date=timezone.now() + timezone.timedelta(days=1),
            priority="LOW",
            user=self.user
        )

    # Test task creation
    def test_create_task(self):
        url = '/tasks/'
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'due_date': timezone.now() + timezone.timedelta(days=1),
            'priority': 'MEDIUM'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
