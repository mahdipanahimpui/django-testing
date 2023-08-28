from django.test import TestCase
from home.models import Writer
from model_bakery import baker

# to partial create model for testing:
# install model_bakery

class TestWriterModel(TestCase):

    # befor every method runs once
    def setup(self):
        # self.writer = Writer.objects.create(
        #     f_name='mahdi',
        #     l_name='panahi',
        #     email='panahi@e.com',
        #     country='iran'
        # )

        # instead use model bakery
        self.writer = baker.make(Writer, f_name='mahdi', l_name='panahi')
        # print(writer.email)

    def test_model_str(self):
        self.assertEqual(str(self.writer), 'mahdi-panahi')
