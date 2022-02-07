from django.test import TestCase
from django.test import client
from django.contrib.auth.models import User


class LoginTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(
            'user', email='user@example.com', password='abcde')
        self.c = client.Client()

    def test_login_and_logout_by_http_protocol(self):
        resp = self.c.get('/restaurants_list/')  # 未登入的訪問
        self.assertRedirects(resp, '/accounts/login/?next=/restaurants_list/')
        # 自行post登入資料至登入網址並檢查重導網頁
        # 使用follow=True取得重新導向路徑
        resp = self.c.post(
            '/accounts/login/', {'username': 'user', 'password': 'abcde'}, follow=True)
        self.assertEqual(resp.redirect_chain, [('/index/', 302)])
        resp = self.c.get('/restaurants_list/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'restaurants_list.html')
        # 自行訪問登出網頁進行登出
        self.c.get('/accounts/logout/')
        resp = self.c.get('/restaurants_list/')
        self.assertRedirects(resp, '/accounts/login/?next=/restaurants_list/')


class IndexWebpageTestCase(TestCase):

    def setUp(self):
        self.c = client.Client()

    def test_index_visiting(self):
        resp = self.c.get('/index/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<p>歡迎來到餐廳王</p>')
        self.assertTemplateUsed(resp, 'index.html')
