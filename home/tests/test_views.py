# from django.test import TestCase, Client, RequestFactory
# from django.urls import reverse
# from django.contrib.auth.models import User, AnonymousUser
# from home.forms import UserRegisterForm
# from home.views import Home


# # Client as an fake client to test mehtods like post get


# class TestUserRegisterView(TestCase):
    
#     def setUp(self):
#         self.client = Client()

#     def test_user_register_GET(self):
#         # client with method GET, requests and an response it return to him
#         response = self.client.get(reverse('home:user_register'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home/register.html') # test the template
#         self.failUnless(response.context['form'], UserRegisterForm) # test the context


#     def test_user_register_POST_valid(self):
#         response = self.client.post(reverse('home:user_register'), data={
#             'username': 'soren',
#             'email': 'soren@e.com',
#             'password': '000',
#             'confirm_password': '000',
#         })
#         self.assertEqual(response.status_code, 302) # redirect code is 302
#         self.assertRedirects(response, reverse('home:home'))
#         # after each test data base destroy
#         self.assertEqual(User.objects.count(), 1)



#     def test_user_register_POST_invalid(self):
#         response = self.client.post(reverse('home:user_register'), data={
#             'username': 'soren',
#             'email': 'invalid_email',
#             'password': '0000',
#             'confirm_password': '0000',
#         })
#         self.assertEqual(response.status_code, 200) # because of form validation render tempale again
#         self.failIf(response.context['form'].is_valid())
#         self.assertFormError(form=response.context['form'], field='email', errors=['Enter a valid email address.'])  
#         # the errors message must be the same as
#         # assertFormError(form, field, errors, msg_prefix='') is for django


# class TestWriterView(TestCase):
    
#     def setUp(self):
#         User.objects.create_user(
#             username='root',
#             email='root@e.com',
#             password='000'
#         )
#         self.client = Client()
#         self.client.login(username='root', email='root@e.com', password='000')


    
#     def test_writers(self):
#         response = self.client.get(reverse('home:writers'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home/writer.html')





# # RequestFactory is used when you want to access the request, not response of the request(like Client())
# # in request authentication is done manually

# class TestHomeView(TestCase):
    
#     def setUp(self):
#         self.user = User.objects.create_user(username='root', email='root@e.com', password='000')
#         self.factory = RequestFactory()


#     def test_home_user_authenticated(self):
#         request = self.factory.get(reverse('home:home'))
#         # authenticate user manually
#         request.user = self.user
#         response = Home.as_view()(request)
#         self.assertEqual(response.status_code, 302) # 302 is redirect


#     def test_home_user_anonymous(self):
#         request = self.factory.get(reverse('home:home'))
#         request.user = AnonymousUser()
#         response = Home.as_view()(request)
#         self.assertEqual(response.status_code, 200) # 200 is render