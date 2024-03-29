from django.db import models

from authentication.models import User

# Create your models here.

class Income(models.Model):
    Source_OPTIONS=[
        ('SALARY','SALARY'),
        ('BUSINESS','BUSINESS'),
        ('SIDE-HUSTLE','SIDE-HUSTLE'),
        ('OTHERS','OTHERS')
    ]

    source = models.CharField(choices = Source_OPTIONS,max_length = 255)
    amount = models.DecimalField(max_digits = 10,decimal_places =2,max_length = 255)
    description = models.TextField()
    owner = models.ForeignKey(to=User,on_delete =models.CASCADE)
    date = models.DateField(null = False,blank = False)

    class Meta:
        ordering:['-date']

    def __str__(self):
        return f'{str(self.owner)}s income'