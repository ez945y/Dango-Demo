from django.test import TestCase
from django.test import client
from zoo import models
from django.test import client
from django.contrib.auth.models import User


class LoginTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(
            'user', email='user@example.com', password='abcde')
        self.c = client.Client()

    def test_login_and_logout(self):
        resp = self.c.get('/restaurants_list/')
        # 未登入的訪問，測試重新導向
        self.assertRedirects(resp, '/accounts/login/?next=/restaurants_list/')
        # Django 內建的登入
        self.c.login(username='user', password='abcde')
        resp = self.c.get('/restaurants_list/')  # 登入後的訪問
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'restaurants_list.html')
        self.c.logout()
        resp = self.c.get('/restaurants_list/')
        self.assertRedirects(resp, '/accounts/login/?next=/restaurants_list/')


class AnimalTestCase(TestCase):
    def test_dog_says(self):
        dog = models.Dog(name="Snoopy")
        self.assertEqual(dog.says(), 'woof')

    def test_cat_says(self):
        cat = models.Cat(name="Garfield")
        self.assertEqual(cat.says(), 'meow')


class IndexWebpageTestCase(TestCase):

    def setUp(self):
        self.c = client.Client()

    def test_index_visiting(self):
        resp = self.c.get('/index/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<p>歡迎來到餐廳王</p>')
        self.assertTemplateUsed(resp, 'index.html')
