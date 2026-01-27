"""
Unit tests for the Flask API
"""

import unittest
import json
from app import app


class FlaskAPITestCase(unittest.TestCase):
    """Test cases for Flask API endpoints"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        """Test home endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_get_tasks(self):
        """Test getting all tasks"""
        response = self.app.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('tasks', data)
        self.assertIsInstance(data['tasks'], list)

    def test_get_task_by_id(self):
        """Test getting a specific task"""
        response = self.app.get('/api/tasks/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('task', data)

    def test_get_nonexistent_task(self):
        """Test getting a task that doesn't exist"""
        response = self.app.get('/api/tasks/9999')
        self.assertEqual(response.status_code, 404)

    def test_create_task(self):
        """Test creating a new task"""
        new_task = {"title": "Test Task", "completed": False}
        response = self.app.post('/api/tasks',
                                  data=json.dumps(new_task),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('task', data)
        self.assertEqual(data['task']['title'], 'Test Task')

    def test_create_task_without_title(self):
        """Test creating a task without required title"""
        response = self.app.post('/api/tasks',
                                  data=json.dumps({}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
