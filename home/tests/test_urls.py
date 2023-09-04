# from django.test import SimpleTestCase, TestCase
# from django.urls import reverse, resolve
# from home.views import Home, About


# # ordei of running tests in django:
# # TestCase , SimpleTestCase, TransactionTestCase, unittest.TestCase


# # could use TestCase
# class TestUrls(SimpleTestCase):

#     def test_home(self):
#         url = reverse('home:home') # convert to /
#         # print(resolve(url))
#         # in resolve: # information of url
#         # ResolverMatch(func=home.views.Home, args=(), kwargs={}, url_name='home', app_names=['home'], namespaces=['home'], route='')
#         self.assertEqual(resolve(url).func.view_class, Home)
#         # view_class returns as a class


#     def test_about(self):
#         url = reverse('home:about', args=('amir',)) # convert to /about/amin
#         self.assertEqual(resolve(url).func.view_class, About)

        