from django.test import TestCase
from .models import Task, Category

class TaskModelTest(TestCase):

    def setUp(self):
        # Setup code to create initial objects
        self.category = Category.objects.create(name="Work")
        self.task = Task.objects.create(
            title="Complete project",
            due_date="2024-12-31",
            category=self.category
        )

    def test_task_creation(self):
        # Test task creation
        self.assertEqual(self.task.title, "Complete project")
        self.assertEqual(self.task.due_date, "2024-12-31")
        self.assertEqual(self.task.completed, False)
        self.assertEqual(self.task.category, self.category)

    def test_task_str(self):
        self.assertEqual(str(self.task), "Complete project")

    def test_task_completed_default(self):
        self.assertEqual(self.task.completed, False)

    def test_task_category_relationship(self):
        self.assertEqual(self.task.category, self.category)

    # generate unit test that checks for an error 
    # if the title is longer than 100 characters
    def test_task_title_length(self):
        task = Task(
            title="a" * 101,
            due_date="2024-12-31",
            category=self.category
        )
        with self.assertRaises(Exception):
            task.full_clean()
            task.save()

