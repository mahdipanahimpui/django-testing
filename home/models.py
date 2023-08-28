from django.db import models

class Writer(models.Model):
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=100)



    # not need to test the fields
    # just needs str 


    def __str__(self):
        return f'{self.f_name}-{self.l_name}'