from django.test import TestCase
from django.urls import reverse


class YourTestCase(TestCase):
    def test_homepage_access(self):
        response = self.client.get(reverse("health_check"))
        self.assertEqual(response.status_code, 200)
