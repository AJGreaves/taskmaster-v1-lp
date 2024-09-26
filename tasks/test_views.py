from django.test import TestCase, Client
from django.urls import reverse
from .models import Task, Category
from .forms import TaskForm

class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        self.category = Category.objects.create(name="Work")
        self.task1 = Task.objects.create(
            title="Task 1",
            due_date="2024-12-31",
            completed=False,
            category=self.category
        )
        self.task2 = Task.objects.create(
            title="Task 2",
            due_date="2024-11-30",
            completed=True,
            category=self.category
        )

    def test_home_view_get(self):
        # Test GET request to home view
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')
        self.assertContains(response, 'Work')
        self.assertIsInstance(response.context['form'], TaskForm)


    def test_home_view_post_valid_form(self):
        # Test POST request with valid form data
        form_data = {
            'title': 'New Task',
            'due_date': '2024-10-10',
            'category': self.category.id
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, self.url)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_home_view_post_invalid_form(self):
        # Test POST request with invalid form data
        response = self.client.post(self.url, {
            'title': 'Test Task',
            'due_date': '2024-12-31',
            # 'category' is missing to make the form invalid
        })
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'category', 'This field is required.')


    def test_home_view_context(self):
        # Test context data in home view
        response = self.client.get(self.url)
        self.assertTrue('to_do_tasks' in response.context)
        self.assertTrue('done_tasks' in response.context)
        self.assertTrue('form' in response.context)

