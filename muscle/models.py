from django.db import models

# Create your models here.
class trainlog(models.Model):
    category_choice=(
        ('chest','胸'),
        ('shoulder','肩'),
        ('spine','背中'),
        ('arm','腕'),
        ('abs','腹'),
        ('leg','脚'),
    )

    used_date=models.DateField('日付')
    category=models.CharField(max_length=100,choices=category_choice)
    comment=models.CharField(max_length=100)
    def __str__(self):
        return str(self.used_date) +'   '+ 'category:'+self.category

class BodyWeight(models.Model):
    used_date=models.DateField('日付')
    weight=models.FloatField(max_length=10)

    def __str__(self):
        return str(self.used_date)+'   Weight:'+str(self.weight)


