from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class Test(TestCase):
    def test_for_homepage(self):
        response = self.client.get(reverse("home"))
        # test that the template used to render the page is the right template
        self.assertTemplateUsed(response, "blog/home.html")
        # test that the page was rendered successfully ie. with a status code of 200
        self.assertEqual(response.status_code, 200)

    def test_for_loginpage(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_for_registerpage(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
