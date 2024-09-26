from django.test import TestCase
from tasks.forms import TaskForm
from tasks.models import Category, Task

class TaskFormTest(TestCase):

    def setUp(self):
        # Setup code to create initial objects
        self.category = Category.objects.create(name="Work")

    def test_task_form_valid_data(self):
        # Test form with valid data
        form_data = {
            'title': 'Complete project',
            'due_date': '2024-12-31',
            'category': self.category.id
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_data(self):
        # Test form with invalid data
        form_data = {
            'title': '',
            'due_date': '',
            'category': ''
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_form_missing_title(self):
        # Test form with missing title
        form_data = {
            'title': '',
            'due_date': '2024-12-31',
            'category': self.category.id
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], ['This field is required.'])


    def test_task_form_missing_due_date(self):
        # Test form with missing due date
        form_data = {
            'title': 'Complete project',
            'due_date': '',
            'category': self.category.id
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['due_date'], ['This field is required.'])

    def test_task_form_missing_category(self):
        # Test form with missing category
        form_data = {
            'title': 'Complete project',
            'due_date': '2024-12-31',
            'category': ''
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['category'], ['This field is required.'])

    def test_task_title_length(self):
        # Test form with title length greater than 50 characters
        form_data = {
            'title': 'a' * 101,
            'due_date': '2024-12-31',
            'category': self.category.id
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'],['Ensure this value has at most 100 characters (it has 101).'])

    def test_task_incorrect_date_format(self):
        # test form with incorrect date format
        form_data = {
            'title': 'Test task',
            'due_date': '2024/12/31',
            'category': self.category.id
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['due_date'],['Enter a valid date.'])