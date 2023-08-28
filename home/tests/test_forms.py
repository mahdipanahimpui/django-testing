from django.test import TestCase
from home.forms import UserRegisterForm
from django.contrib.auth.models import User
import random

class CreateUser:
    def __init__(self):
        rand = random.randint(1, 100000)
        self.u = f'root{rand}'
        self.e = f'{self.u}@e.com'
        self.p = '000'
        self.cp = '000'

muser = CreateUser()



class TestRegisterForm(TestCase):

    # this method is used to create data when object of TestRegisterForm class is created
    # for data that is wont change in future, runs befor all tests
    @classmethod
    def setUpTestData(self):
        User.objects.create_user(username=muser.u, email=muser.e, password=muser.p)


    def test_valid_data(self):
        form = UserRegisterForm(data={'username':'jack', 'email':'jack@e.com', 'password':'1', 'confirm_password':'1'})
        self.assertTrue(form.is_valid())


    def test_empty_data(self):
        form = UserRegisterForm(data={'username': 'me'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


    
    def test_exist_email(self):
        user = CreateUser()
        form = UserRegisterForm(data={
            'username':f'not-{user.u}', 'email':muser.e, 'password': user.p, 'confirm_password': user.cp
        })

        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('email'))



    def test_unmatch_password(self):
        user = CreateUser()
        form = UserRegisterForm(
            data={
                'username': user.u,
                'email': user.e,
                'password': user.p,
                'confirm_password': 'nono'
            }
        )
        self.assertEqual(len(form.errors), 1)
        self.assertTemplateNotUsed(form.has_error) # dont use has_error('confirm_password'),
        # because password validation, is form level validation not field level validation